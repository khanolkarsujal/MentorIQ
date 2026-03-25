import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "mentors.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create mentors table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mentors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        title TEXT NOT NULL,
        company TEXT,
        avatar_url TEXT,
        tech_stack TEXT
    )
    """)
    
    # Check if empty, then seed
    cursor.execute("SELECT COUNT(*) FROM mentors")
    if cursor.fetchone()[0] == 0:
        seed_mentors(cursor)
        
    conn.commit()
    conn.close()

def seed_mentors(cursor):
    initial_mentors = [
        ("Sarah Jenkins", "Senior Backend Engineer", "Google", "https://ui-avatars.com/api/?name=Sarah+Jenkins&background=random", ["Python", "Go", "Docker", "AWS", "FastAPI"]),
        ("David Chen", "Lead Frontend Developer", "Netflix", "https://ui-avatars.com/api/?name=David+Chen&background=random", ["JavaScript", "React", "TypeScript", "Next.js", "CSS"]),
        ("Amelia Rodriguez", "Staff DevOps Engineer", "Stripe", "https://ui-avatars.com/api/?name=Amelia+Rodriguez&background=random", ["Kubernetes", "Docker", "CI/CD", "Terraform", "Go"]),
        ("James Wilson", "Full Stack Engineer", "Meta", "https://ui-avatars.com/api/?name=James+Wilson&background=random", ["React", "Node.js", "GraphQL", "PostgreSQL", "JavaScript"]),
        ("Maria Garcia", "Machine Learning Engineer", "OpenAI", "https://ui-avatars.com/api/?name=Maria+Garcia&background=random", ["Python", "PyTorch", "TensorFlow", "CUDA"]),
        ("Chen Wei", "Cloud Architect", "Amazon", "https://ui-avatars.com/api/?name=Chen+Wei&background=random", ["AWS", "Python", "Serverless", "DynamoDB"]),
        ("Taylor Singh", "Data Engineer", "Snowflake", "https://ui-avatars.com/api/?name=Taylor+Singh&background=random", ["Python", "SQL", "Spark", "Kafka", "Data Modeling"]),
        ("Priya Patel", "Senior Mobile Engineer", "Uber", "https://ui-avatars.com/api/?name=Priya+Patel&background=random", ["Swift", "Kotlin", "React Native", "iOS", "Android"]),
        ("Alex Mercer", "Staff Backend Engineer", "Discord", "https://ui-avatars.com/api/?name=Alex+Mercer&background=random", ["Rust", "C++", "Go", "System Design", "Python"]),
        ("Jordan Lee", "Principal Engineer", "Microsoft", "https://ui-avatars.com/api/?name=Jordan+Lee&background=random", ["C#", ".NET", "Azure", "System Architecture", "TypeScript"])
    ]
    
    for m in initial_mentors:
        cursor.execute(
            "INSERT INTO mentors (name, title, company, avatar_url, tech_stack) VALUES (?, ?, ?, ?, ?)",
            (m[0], m[1], m[2], m[3], json.dumps(m[4]))
        )
        
def find_best_mentors(title_query, user_tech_stack, limit=2):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # We fetch all and do a simple in-memory scoring since the DB is very small.
    cursor.execute("SELECT * FROM mentors")
    all_mentors = cursor.fetchall()
    conn.close()
    
    if not all_mentors:
        return []
        
    scored_mentors = []
    
    title_query_lower = title_query.lower()
    user_tech_lower = [t.lower() for t in user_tech_stack]
    
    for row in all_mentors:
        mentor = dict(row)
        mentor["tech_stack"] = json.loads(mentor["tech_stack"])
        
        score = 0
        mentor_title_lower = mentor["title"].lower()
        
        # 1. Match title (e.g., if LLM recommends "Backend Engineer" and mentor is "Senior Backend Engineer")
        if title_query_lower in mentor_title_lower or mentor_title_lower in title_query_lower:
            score += 50
        
        # 2. Match tech stack
        mentor_tech_lower = [t.lower() for t in mentor["tech_stack"]]
        overlap = set(user_tech_lower).intersection(set(mentor_tech_lower))
        score += len(overlap) * 10 
        
        mentor["score"] = score
        scored_mentors.append(mentor)
        
    # Sort by descending score
    scored_mentors.sort(key=lambda x: x["score"], reverse=True)
    return scored_mentors[:limit]

if __name__ == "__main__":
    init_db()
    print("Database initialized with mentors.")

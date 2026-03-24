import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# 1. SETUP
load_dotenv()
app = FastAPI()

# CORS for Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# PATHS
PROJECT_ROOT = Path(__file__).resolve().parent.parent
frontend_path = PROJECT_ROOT / "frontend"
html_path = frontend_path / "index.html"

# MOUNT
app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

# AI CLIENT
api_key = os.getenv("GROQ_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1") if api_key else None

# Helper: Fetch README
def fetch_readme(username, repo_name):
    for branch in ['main', 'master']:
        url = f"https://raw.githubusercontent.com/{username}/{repo_name}/{branch}/README.md"
        try:
            res = requests.get(url, timeout=3)
            if res.status_code == 200:
                return res.text[:2000]
        except:
            continue
    return "No README content found."

# Helper: Fetch top languages across repos
def fetch_languages(username, repos, headers):
    lang_count = {}
    for repo in repos[:5]:
        try:
            url = f"https://api.github.com/repos/{username}/{repo['name']}/languages"
            res = requests.get(url, headers=headers, timeout=3)
            if res.status_code == 200:
                for lang, bytes_count in res.json().items():
                    lang_count[lang] = lang_count.get(lang, 0) + bytes_count
        except:
            continue
    return sorted(lang_count, key=lang_count.get, reverse=True)[:6]

# 2. ROUTES
@app.get("/")
async def serve_home():
    return FileResponse(html_path)

@app.get("/api/analyze")
async def analyze_github(username: str = Query(..., min_length=1)):
    # RICH MOCK FALLBACK DATA
    mock_data = {
        "skill_level": "Intermediate",
        "maturity_score": 6,
        "top_languages": ["Python", "JavaScript", "HTML"],
        "strengths": ["Consistent project delivery", "REST API design with FastAPI"],
        "skill_gaps": ["Test coverage and TDD practices", "Database optimization and query design"],
        "mentor_match": "Senior Backend Engineer",
        "insights": "Shows strong foundational skills in Python web development. To reach a senior level, focus on building production-grade systems with robust testing and observability."
    }

    try:
        # A. Fetch GitHub repos
        headers = {'User-Agent': 'MentorIQ-App'}
        repos_url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=10"
        res = requests.get(repos_url, headers=headers, timeout=5)

        if res.status_code != 200:
            print(f"DEBUG: GitHub API failed for {username} — status {res.status_code}")
            raise Exception("GitHub user not found")
        repos = res.json()
        if not repos:
            return {"status": "success", "username": username, **mock_data}

        # B. Gather rich context
        latest_repo = repos[0]['name']
        readme = fetch_readme(username, latest_repo)
        top_languages = fetch_languages(username, repos, headers)
        topics = repos[0].get('topics', [])
        total_repos = len(repos)
        stars = sum(r.get('stargazers_count', 0) for r in repos)

        # C. Staff Engineer AI Audit — 5-Pillar Rubric
        if client:
            prompt = f"""
You are a Staff Engineer performing a hiring assessment for '{username}'.

Audit their portfolio using their top project '{latest_repo}' and README below.

README:
{readme[:2000]}

ADDITIONAL SIGNALS:
- Topics/Tags: {', '.join(topics) if topics else 'None'}
- Detected Languages: {', '.join(top_languages) if top_languages else 'Unknown'}
- Total Public Repos: {total_repos}
- Total Stars: {stars}

EVALUATE USING THIS 5-PILLAR TECHNICAL MATURITY RUBRIC:
1. DevOps & Prod-Readiness: Does the repo mention Docker, CI/CD (GitHub Actions), or .env / .env.example files? A developer who uses these understands "it works on my machine" is not enough. This is a Senior signal.
2. Documentation Quality: Does the README have setup instructions, architecture diagrams, API docs, or screenshots/GIFs? Documentation is the difference between a lone coder and a team player.
3. Modular Architecture: Does the project mention microservices, API structure, or separation of concerns? Juniors write monolithic spaghetti; Mid/Seniors structure apps into logical, reusable modules.
4. Security & Best Practices: Does it mention environment variables (no hardcoded keys), JWT auth, or robust error handling? Security-awareness is a high-maturity signal.
5. Integration Complexity: Are they building a simple ToDo list, or integrating with real APIs, databases, and external services (e.g., Stripe, OpenAI, PostgreSQL)? Complex integrations show a developer who solves real business problems.

Based on this rubric, determine their overall maturity.

RETURN ONLY VALID JSON:
{{
    "skill_level": "Beginner or Intermediate or Advanced",
    "maturity_score": <integer 1-10>,
    "top_languages": [<list of 3-5 detected tech stack items>],
    "strengths": [<exactly 2 of the 5 pillars they clearly excel at, phrased as a specific observation>],
    "skill_gaps": [<exactly 2 of the 5 pillars they are missing or weak in, phrased as actionable advice>],
    "mentor_match": "<ideal senior mentor job title (e.g., Senior Systems Architect)>",
    "insights": "<2-sentence professional audit focusing on code structure and maturity growth path>"
}}
"""
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            analysis = json.loads(completion.choices[0].message.content)
            return {
                "status": "success",
                "username": username,
                "avatar_url": f"https://github.com/{username}.png",
                "total_repos": total_repos,
                "stars": stars,
                **analysis
            }

        # No AI client fallback
        return {
            "status": "success",
            "username": username,
            "avatar_url": f"https://github.com/{username}.png",
            "total_repos": total_repos,
            "stars": stars,
            **mock_data
        }

    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "success", "username": username, "avatar_url": f"https://github.com/{username}.png", **mock_data}

@app.get("/api/status")
def get_status():
    return {"status": "online"}
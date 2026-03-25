import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import re
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import mentor_db

# 1. SETUP
load_dotenv()
app = FastAPI()

# Init Database
mentor_db.init_db()

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
    return sorted(lang_count, key=lambda x: lang_count[x], reverse=True)[:6]

# Helper: Deep Repo Context
def fetch_deep_repo_context(username, repo_name, headers):
    context = {"file_structure": [], "recent_commits": [], "recent_prs": [], "recent_issues": []}
    
    # 1. File Structure (Tree)
    try:
        url = f"https://api.github.com/repos/{username}/{repo_name}/git/trees/main?recursive=1"
        res = requests.get(url, headers=headers, timeout=3)
        if res.status_code == 404:
            url = f"https://api.github.com/repos/{username}/{repo_name}/git/trees/master?recursive=1"
            res = requests.get(url, headers=headers, timeout=3)
        if res.status_code == 200:
            tree = res.json().get('tree', [])
            paths = [item['path'] for item in tree if item['type'] == 'tree' or item['path'].endswith(('.py', '.js', '.ts', '.java', '.go', '.json', 'Dockerfile', '.yml', '.md', '.html', '.css')) or 'docker' in item['path'].lower() or '.vscode' in item['path']]
            context['file_structure'] = paths[:100]
    except:
        pass

    # 2. Commits
    try:
        url = f"https://api.github.com/repos/{username}/{repo_name}/commits?per_page=5"
        res = requests.get(url, headers=headers, timeout=3)
        if res.status_code == 200:
            context['recent_commits'] = [c['commit']['message'] for c in res.json()]
    except:
        pass

    # 3. Pull Requests
    try:
        url = f"https://api.github.com/repos/{username}/{repo_name}/pulls?state=all&per_page=3"
        res = requests.get(url, headers=headers, timeout=3)
        if res.status_code == 200:
            context['recent_prs'] = [pr['title'] for pr in res.json()]
    except:
        pass

    # 4. Issues
    try:
        url = f"https://api.github.com/repos/{username}/{repo_name}/issues?state=all&per_page=3"
        res = requests.get(url, headers=headers, timeout=3)
        if res.status_code == 200:
            context['recent_issues'] = [issue['title'] for issue in res.json() if 'pull_request' not in issue]
    except:
        pass

    return context

# 2. ROUTES
@app.get("/")
async def serve_home():
    return FileResponse(html_path)

@app.get("/api/analyze")
async def analyze_github(username: str = Query(..., min_length=1)):
    # Sanitize username: only allow alphanumeric, hyphen, and dot (valid GitHub chars)
    username = re.sub(r'[^a-zA-Z0-9\-.]', '', username)
    if not username:
        raise HTTPException(status_code=400, detail="Invalid username. Only alphanumeric characters, hyphens and dots are allowed.")
    if len(username) > 39:  # GitHub max username length
        raise HTTPException(status_code=400, detail="Username too long. Max 39 characters.")

    try:
        # A. Fetch GitHub repos
        headers = {'User-Agent': 'GitMentor-App'}
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token:
            headers['Authorization'] = f"token {github_token}"
            
        repos_url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=10"
        res = requests.get(repos_url, headers=headers, timeout=5)

        if res.status_code == 403 or res.status_code == 429:
            return {"status": "error", "detail": "GitHub API Rate Limit exceeded. Please configure GITHUB_TOKEN in backend/.env"}
            
        if res.status_code != 200:
            print(f"DEBUG: GitHub API failed for {username} — status {res.status_code}")
            return {"status": "error", "detail": f"GitHub user '{username}' not found or API error."}
            
        res_json = res.json()
        if type(res_json) is dict and "message" in res_json:
            repos = []
        else:
            repos = res_json

        if not repos:
            return {"status": "error", "detail": f"User '{username}' has no public repositories to analyze."}

        # B. Gather rich context
        latest_repo = repos[0]['name']
        readme = fetch_readme(username, latest_repo)
        top_languages = fetch_languages(username, repos, headers)
        topics = repos[0].get('topics', [])
        total_repos = len(repos)
        stars = sum(r.get('stargazers_count', 0) for r in repos)

        repo_summaries = []
        for r in sorted(repos, key=lambda x: x.get('stargazers_count', 0), reverse=True)[:5]:
            repo_summaries.append(f"{r.get('name')} (Stars: {r.get('stargazers_count', 0)}): {r.get('description', 'No description')}")

        # C. Gather deep context
        deep_context = fetch_deep_repo_context(username, latest_repo, headers)

        # D. Staff Engineer AI Audit — Deep 5-Pillar Rubric
        if client:
            prompt = f"""
You are a Staff Engineer performing a hiring assessment for '{username}'.

Audit their portfolio utilizing their Github Repo Context for '{latest_repo}'.

README:
{readme[:2000]}

DEEP CONTEXT (FILE STRUCTURE, AST/DEPENDENCIES, COMMITS, PRs, ISSUES):
- File Structure (AST Proxy): {deep_context['file_structure']}
- Recent Commits: {deep_context['recent_commits']}
- Recent PRs: {deep_context['recent_prs']} 
- Recent Issues: {deep_context['recent_issues']}

ADDITIONAL SIGNALS:
- Topics/Tags: {', '.join(topics) if topics else 'None'}
- Detected Languages: {', '.join(top_languages) if top_languages else 'Unknown'}
- Repositories context: {repo_summaries}
- Total Public Repos: {total_repos}
- Total Stars: {stars}

EVALUATE USING THESE 5 METRICS (SCORE 0-100 EACH). DO NOT HALLUCINATE OR GUESS. Use strictly the provided JSON structure.
If there are no open source contributions, say "No significant open source contributions detected." 
If you see Dockerfiles or .vscode folders in the file structure, list them under technologies_used.
1. Code Quality (0.25 weight): Error handling, readability, module imports.
2. Architecture & File Structure (0.20 weight): Project layout, microservices, logical boundaries.
3. Engineering Practices (0.20 weight): CI/CD configs, Dockerfiles, branching patterns via commits, PR descriptions.
4. Project Depth (0.20 weight): Complexity of external dependencies seen in file structure, integration logic.
5. Problem Solving (0.15 weight): Evidenced by issue tracking, PR resolutions, commit topics.

RETURN ONLY VALID JSON:
{{
    "github_profile_level": "<Beginner, Intermediate, Advanced, or Professional>",
    "coding_skills_level": "<Beginner, Intermediate, Advanced, or Professional>",
    "project_quality_level": "<Beginner, Intermediate, Advanced, or Professional>",
    "top_3_repos": ["<repo1>", "<repo2>", "<repo3>"],
    "open_source_contributions": "<Summary of open source contributions and impact>",
    "technologies_used": ["<Search strictly for all tools used, including VS/VS Code, Docker, Frameworks>"],
    "subscores": {{
        "code_quality": <0-100>,
        "architecture": <0-100>,
        "engineering_practices": <0-100>,
        "project_depth": <0-100>,
        "problem_solving": <0-100>
    }},
    "strengths": [<exactly 2 strengths based on file structure and deeper analysis>],
    "skill_gaps": [<exactly 2 gaps based on deeper analysis>],
    "mentor_match": "<ideal senior mentor job title>",
    "insights": "<2-sentence audit focusing on code structure, architecture, and maturity>"
}}
"""
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            analysis = json.loads(completion.choices[0].message.content)
            
            sub = analysis.get('subscores', {})
            score_raw = (
                0.25 * sub.get('code_quality', 50) +
                0.20 * sub.get('architecture', 50) +
                0.20 * sub.get('engineering_practices', 50) +
                0.20 * sub.get('project_depth', 50) +
                0.15 * sub.get('problem_solving', 50)
            )
            # score_raw is 0-100; convert to 0-10 scale for display
            score = round(score_raw / 10.0, 1)
            
            if score <= 3.0:
                skill_level = "Beginner"
            elif score <= 5.0:
                skill_level = "Intermediate"
            elif score <= 7.0:
                skill_level = "Advanced"
            else:
                skill_level = "Professional"
                
            if 'subscores' in analysis:
                del analysis['subscores']

            # Query the database for a matching mentor
            job_title = analysis.get('mentor_match', '')
            user_tools = analysis.get('technologies_used', [])
            matched_mentors = mentor_db.find_best_mentors(job_title, user_tools, limit=1)
            
            if matched_mentors:
                analysis['matched_mentor'] = matched_mentors[0]
            else:
                analysis['matched_mentor'] = None

            return {
                "status": "success",
                "username": username,
                "avatar_url": f"https://github.com/{username}.png",
                "total_repos": total_repos,
                "stars": stars,
                "maturity_score": score,
                "skill_level": skill_level,
                **analysis
            }

        # No AI client fallback
        return {
            "status": "error",
            "detail": "GROQ_API_KEY not configured. Cannot perform AI Audit."
        }

    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "error", "detail": f"Analysis failed: {str(e)}"}

@app.get("/api/status")
def get_status():
    return {"status": "online"}
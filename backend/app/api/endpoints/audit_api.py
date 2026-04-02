import requests
import re
from fastapi import APIRouter, Query, HTTPException # type: ignore
from app.services.github_service import GitHubService
from app.services.audit_service import audit_service
from app.db import database
from app.core.config import settings

router = APIRouter()

@router.get("/analyze")
async def analyze_github(username: str = Query(..., min_length=1)):
    # 1. Sanitize
    username = re.sub(r'[^a-zA-Z0-9\-.]', '', username)
    if len(username) > 39:
        raise HTTPException(status_code=400, detail="Username too long.")

    # 2. Setup Headers
    headers = {'User-Agent': 'MentorIQ-Audit'}
    if settings.GITHUB_TOKEN:
        headers['Authorization'] = f"token {settings.GITHUB_TOKEN}"

    # 3. Fetch Data (API -> Fallback)
    repos_url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=10"
    res = requests.get(repos_url, headers=headers, timeout=5)
    
    if res.status_code in [403, 429]:
        repos = GitHubService.scrape_fallback(username)
    elif res.status_code != 200:
        raise HTTPException(status_code=404, detail="GitHub user not found.")
    else:
        repos = res.json()

    if not repos:
        raise HTTPException(status_code=404, detail="No public repositories found.")

    # 4. Context Gathering
    latest_repo = repos[0].get('name', '')
    readme = GitHubService.fetch_readme(username, latest_repo)
    langs = GitHubService.fetch_languages(username, repos)
    deep_context = GitHubService.get_deep_context(username, latest_repo)
    
    # Summarize Repos for AI
    repo_summaries = [f"{r.get('name')}: {r.get('description', '')}" for r in repos[:5]]

    # 5. Perform AI Audit
    analysis = audit_service.perform_audit(
        username, latest_repo, readme, deep_context, langs, repo_summaries
    )

    # 6. Mentor Matchmaking
    mentor_job = analysis.get('mentor_match', '')
    user_tools = analysis.get('technologies_used', [])
    matched = database.find_best_mentors(mentor_job, user_tools)

    return {
        "status": "success",
        "username": username,
        "maturity_score": analysis.get('maturity_score', 0),
        "avatar_url": f"https://github.com/{username}.png",
        "matched_mentor": matched[0] if matched else None,
        **analysis
    }

@router.get("/status")
def get_status():
    return {"status": "online", "api_v": "v1.1-saas"}

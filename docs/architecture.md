# MentorIQ — System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT BROWSER                          │
│         HTML + CSS + JS (Vanilla, no framework required)        │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTP GET /api/analyze?username=…
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     NGINX (Reverse Proxy)                       │
│                  Port 80 → Port 8000 (internal)                 │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FastAPI Backend  (backend/main.py)             │
│                                                                 │
│  ┌──────────────────┐    ┌──────────────────────────────────┐  │
│  │  GitHub API Call │    │  5-Pillar Prompt Builder         │  │
│  │                  │    │  • DevOps / CI-CD signals        │  │
│  │  /users/{u}/repos│    │  • Documentation quality         │  │
│  │  Top 5 langs     │    │  • Modular architecture          │  │
│  │  README fetch    │    │  • Security best practices       │  │
│  │  Stars, topics   │    │  • Integration complexity        │  │
│  └────────┬─────────┘    └──────────────┬───────────────────┘  │
│           └──────────────────┬──────────┘                       │
│                              ▼                                   │
│              ┌───────────────────────────┐                      │
│              │  Groq API (Llama-3.3-70b) │                      │
│              │  JSON-mode enforced output │                      │
│              └───────────────────────────┘                      │
│                              │                                   │
│           Returns: skill_level, maturity_score, top_languages,  │
│                   strengths, skill_gaps, mentor_match, insights  │
└─────────────────────────────────────────────────────────────────┘
```

## Key Technical Decisions

| Decision | Rationale |
|---|---|
| **FastAPI** over Flask | Async support, native Pydantic validation, auto-generated OpenAPI docs |
| **Groq / Llama-3.3-70b** | Sub-second inference — critical for demo; outperforms GPT-3.5 in structured JSON output |
| **JSON-mode** on LLM call | Guarantees parseable output — eliminates brittle regex parsing |
| **`response_format=json_object`** | Forces schema compliance without post-processing |
| **Multi-repo language fetch** | Aggregates across top 5 repos for accurate stack fingerprint |
| **Mock fallback data** | Graceful degradation if GitHub API or Groq is unavailable |

## Technical Challenges Faced & Solutions

### 1. LLM Model Decommission
**Problem:** The initial `llama3-8b-8192` model was decommissioned by Groq mid-development, causing all analysis calls to silently fail and return mock data.  
**Solution:** Upgraded to `llama-3.3-70b-versatile`, added `traceback.print_exc()` logging, and confirmed live responses with `curl`.

### 2. AI Hallucination on Generic Profiles  
**Problem:** With little context (empty README), the LLM returned generic "Python developer" responses.  
**Solution:** Added 5 contextual signals to the prompt: language distribution across 5 repos, star count, GitHub Topics, repo count, and README content. Richer context = less hallucination.

### 3. Secret Accidentally Committed to Git  
**Problem:** `.env` file was committed before `.gitignore` was configured, causing GitHub to block the push.  
**Solution:** Used `git-filter-repo` to permanently purge the file from all commit history, then force-pushed. Rotated the API key immediately.

### 4. Result Container Missing (UI Hang)  
**Problem:** `script.js` referenced `#result-display` which didn't exist in the initial HTML, causing the "Analyzing..." spinner to hang forever.  
**Solution:** Added `<div id="result-display"></div>` to the HTML. Now also validated with `document.getElementById` null-checks.

## Security Considerations

- All secrets managed via `.env` / environment variables — never hardcoded
- `.env` excluded from git via `.gitignore` 
- CORS configured to restrict origins in production
- Input validated server-side via FastAPI `Query(min_length=1)`
- Rate limiting ready via `slowapi` (see `requirements.txt`)

## Running Tests

```bash
pip install pytest httpx
pytest tests/ -v
```

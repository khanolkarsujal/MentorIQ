import json
import os
from openai import OpenAI # type: ignore
from app.core.config import settings

class AuditService:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.client = OpenAI(api_key=self.api_key, base_url="https://api.groq.com/openai/v1") if self.api_key else None

    def perform_audit(self, username: str, latest_repo: str, readme: str, deep_context: dict, tools: list, repos_context: list):
        if not self.client:
            return {"status": "error", "detail": "GROQ_API_KEY Missing"}


        prompt = f"""
        Principal Engineer Audit for '{username}' (Repo: '{latest_repo}').
        Context: README ({len(readme)} char), Files ({deep_context['file_structure']}), Tech ({tools}).
        All Repos: {repos_context}.

        
        Evaluate 5 metrics (0-100 score). BE STRICT AND REALISTIC.
        - Only label as 'High' or 'Professional' if there is clear production-grade code (tests, clear architecture).
        - Use 'Low' or 'Junior' for academic or simple projects.
        
        1. Code Quality (0.25)
        2. Architecture (0.20)
        3. Engineering Practices (0.20)
        4. Project Depth (0.20)
        5. Problem Solving (0.15)

        
        RETURN JSON:
        {{
            "github_profile_level": "<Beginner/Intermediate/Advanced>",
            "coding_skills_level": "<Junior/Mid/Senior/Expert>",
            "project_quality_level": "<Low/Moderate/High/Professional>",
            "subscores": {{ "code_quality": 0, "architecture": 0, "engineering_practices": 0, "project_depth": 0, "problem_solving": 0 }},
            "strengths": ["...", "..."],
            "skill_gaps": ["...", "..."],
            "technologies_used": ["Python", "Docker", "..."],
            "top_3_repos": ["Repo1", "Repo2", "Repo3"],
            "open_source_contributions": "A summary of any visible open source or community impact.",
            "mentor_match": "Senior DevOps Engineer",
            "insights": "...",
            "activity_overview": "..."
        }}


        """
        
        completion = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        analysis = json.loads(completion.choices[0].message.content)
        
        # Calculate Weighted Maturity Score (0-10)
        sub = analysis.get('subscores', {})
        score_raw = (
            0.25 * sub.get('code_quality', 50) +
            0.20 * sub.get('architecture', 50) +
            0.20 * sub.get('engineering_practices', 50) +
            0.20 * sub.get('project_depth', 50) +
            0.15 * sub.get('problem_solving', 50)
        )
        analysis['maturity_score'] = float(f"{(score_raw / 10.0):.1f}")
        
        return analysis

# Singleton instance for the service
audit_service = AuditService()

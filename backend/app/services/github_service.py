import requests
import itertools # type: ignore
from typing import List, Dict, Any, cast
from bs4 import BeautifulSoup # type: ignore
from app.core.config import settings

class GitHubService:
    @staticmethod
    def fetch_readme(username: str, repo_name: str) -> str:
        headers = {'User-Agent': 'Mozilla/5.0'}
        for branch in ['main', 'master']:
            url = f"https://raw.githubusercontent.com/{username}/{repo_name}/{branch}/README.md"
            try:
                res = requests.get(url, headers=headers, timeout=3)
                if res.status_code == 200:
                    return res.text[:2000]
            except:
                continue
        return "No README content found."

    @staticmethod
    def scrape_fallback(username: str) -> List[Dict[str, Any]]:
        url = f"https://github.com/{username}?tab=repositories"
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code != 200: return []
            soup = BeautifulSoup(res.text, 'html.parser')
            repos: List[Dict[str, Any]] = []
            for li in soup.find_all('li', itemprop='owns'):
                name_tag = li.find('a', itemprop='name codeRepository')
                if not name_tag: continue
                repos.append({
                    'name': name_tag.text.strip(),
                    'description': li.find('p', itemprop='description').text.strip() if li.find('p', itemprop='description') else '',
                    'stargazers_count': 0, 
                    'language': li.find('span', itemprop='programmingLanguage').text.strip() if li.find('span', itemprop='programmingLanguage') else 'Unknown',
                    'topics': [] 
                })
            return repos
        except:
            return []

    @staticmethod
    def fetch_languages(username: str, repos: List[Dict[str, Any]]) -> List[str]:
        lang_count = {}
        headers = {'User-Agent': 'MentorIQ-Audit'}
        if settings.GITHUB_TOKEN:
            headers['Authorization'] = f"token {settings.GITHUB_TOKEN}"

        for repo in repos[:5]:
            try:
                url = f"https://api.github.com/repos/{username}/{repo['name']}/languages"
                res = requests.get(url, headers=headers, timeout=3)
                if res.status_code == 200:
                    for lang, bytes_count in res.json().items():
                        lang_count[lang] = lang_count.get(lang, 0) + bytes_count
            except:
                continue
        
        langs_sorted = sorted(lang_count, key=lambda x: lang_count[x], reverse=True)
        return list(itertools.islice(langs_sorted, 6))

    @staticmethod
    def get_deep_context(username: str, repo_name: str) -> Dict[str, Any]:
        context = {"file_structure": [], "recent_commits": [], "recent_prs": [], "recent_issues": []}
        headers = {'User-Agent': 'MentorIQ-Audit'}
        if settings.GITHUB_TOKEN:
            headers['Authorization'] = f"token {settings.GITHUB_TOKEN}"

        # Logic for File Structure, Commits, PRs, etc.
        try:
            url = f"https://api.github.com/repos/{username}/{repo_name}/git/trees/main?recursive=1"
            res = requests.get(url, headers=headers, timeout=3)
            if res.status_code == 404:
                url = f"https://api.github.com/repos/{username}/{repo_name}/git/trees/master?recursive=1"
                res = requests.get(url, headers=headers, timeout=3)
            if res.status_code == 200:
                tree = res.json().get('tree', [])
                paths = [str(item.get('path', '')) for item in cast(List[Dict[str, Any]], tree) if item.get('type') == 'blob']
                context['file_structure'] = list(itertools.islice(paths, 25))
        except: pass

        # Shortened for clean SaaS structure
        return context

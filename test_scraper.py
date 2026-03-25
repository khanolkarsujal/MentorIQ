import requests
from bs4 import BeautifulSoup

def get_contributions(username):
    try:
        url = f"https://github.com/{username}?tab=overview"
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Last year / this year
        h2 = soup.find('h2', class_='f4 text-normal mb-2')
        if h2:
            return h2.text.strip()
        return "Not found"
    except Exception as e:
        return str(e)

print(get_contributions('torvalds'))

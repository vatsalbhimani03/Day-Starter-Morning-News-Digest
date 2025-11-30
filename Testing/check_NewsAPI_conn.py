import os, sys, requests
from config import NEWS_API

url = "https://newsapi.org/v2/top-headlines"
params = {"country": "us", "category": "technology", "pageSize": 5}
headers = {"X-Api-Key": NEWS_API}

r = requests.get(url, params=params, headers=headers, timeout=15)
print("HTTP", r.status_code, "| endpoint:", r.url)
data = r.json()

for i, a in enumerate(data.get("articles", [])[:5], 1):
    title = (a.get("title") or "").strip()
    src = ((a.get("source") or {}).get("name") or "").strip()
    print(f"{i}. {title}  [{src}]")

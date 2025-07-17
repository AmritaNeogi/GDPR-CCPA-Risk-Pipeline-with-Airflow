# scripts/fetch_policy_data.py

import os, requests, json
from bs4 import BeautifulSoup
from datetime import datetime

RAW_DIR = os.path.join(os.path.dirname(__file__), "../data/raw")

def fetch_policy_data():
    url = "https://edpb.europa.eu/news/news_en"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    articles = []
    for row in soup.select("div.views-row"):
        title_el = row.select_one("h4.node__title a")
        date_el  = row.select_one("span.news-date")
        if not title_el or not date_el:
            continue
        articles.append({
            "title": title_el.get_text(strip=True),
            "link":  "https://edpb.europa.eu" + title_el["href"],
            "date":  date_el.get_text(strip=True),
        })

    if not articles:
        print("❌ No articles found on EDPB news page.")
        return

    os.makedirs(RAW_DIR, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_path = os.path.join(RAW_DIR, f"edpb_news_{ts}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2)

    print(f"✅ Scraped and saved {len(articles)} articles to {out_path}")

if __name__ == "__main__":
    fetch_policy_data()

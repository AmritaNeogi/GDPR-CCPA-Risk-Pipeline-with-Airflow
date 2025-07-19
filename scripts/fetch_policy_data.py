# scripts/fetch_policy_data.py

import os, requests, json, time
from bs4 import BeautifulSoup
from datetime import datetime

RAW_DIR = os.path.join(os.path.dirname(__file__), "../data/raw")
BASE_URL = "https://edpb.europa.eu"

# Config: how many pages to scrape (each has ~10 articles)
NUM_PAGES = 15  # ~150 articles total

def fetch_policy_data():
    all_articles = []

    for page in range(NUM_PAGES):
        print(f"🔄 Fetching page {page+1}/{NUM_PAGES}...")
        url = f"{BASE_URL}/news/news_en?page={page}"
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"⚠️ Error fetching page {page}: {e}")
            continue

        soup = BeautifulSoup(resp.text, "lxml")
        rows = soup.select("div.views-row")

        for row in rows:
            title_el = row.select_one("h4.node__title a")
            date_el  = row.select_one("span.news-date")
            if not title_el or not date_el:
                continue

            all_articles.append({
                "title": title_el.get_text(strip=True),
                "link": BASE_URL + title_el["href"],
                "date": date_el.get_text(strip=True)
            })

        time.sleep(0.5)  # be polite to the server

    if not all_articles:
        print("❌ No articles found across pages.")
        return

    os.makedirs(RAW_DIR, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_path = os.path.join(RAW_DIR, f"edpb_news_{ts}.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, indent=2)

    print(f"✅ Scraped {len(all_articles)} articles across {NUM_PAGES} pages")
    print(f"📁 Saved to: {out_path}")

if __name__ == "__main__":
    fetch_policy_data()

# scripts/fetch_policy_data.py

import requests
import os
import json
from datetime import datetime

# Directory where raw data will be saved
RAW_DIR = os.path.join(os.path.dirname(__file__), "../data/raw")

def fetch_policy_data():
    """
    Download GDPR/CCPA policy updates (RSS XML) and save
    to data/raw with a timestamped filename.
    """
    url = "https://www.dataprotectionreport.com/feed/"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/138.0.0.0 Safari/537.36"
        )
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        raw_bytes = resp.content
        print("Fetched real data from URL.")
    except Exception as e:
        print(f"Warning: could not fetch from {url} ({e}). Writing dummy data instead.")
        dummy = {
            "policies": [
                {
                    "source": "GDPR",
                    "title": "Sample GDPR update",
                    "date": datetime.utcnow().isoformat()
                }
            ]
        }
        raw_bytes = json.dumps(dummy, indent=2).encode("utf-8")

    # ensure raw directory exists
    os.makedirs(RAW_DIR, exist_ok=True)

    # save the file (using .xml extension for RSS or dummy JSON)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    out_path = os.path.join(RAW_DIR, f"policy_updates_{ts}.xml")
    with open(out_path, "wb") as f:
        f.write(raw_bytes)

    print(f"Saved raw policy data to {out_path}")

if __name__ == "__main__":
    fetch_policy_data()

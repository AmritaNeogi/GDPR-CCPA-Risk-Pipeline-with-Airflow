# scripts/process_policy_data.py

import os
import json
import glob
import csv
import xml.etree.ElementTree as ET
from datetime import datetime

RAW_DIR = os.path.join(os.path.dirname(__file__), "../data/raw")
PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "../data/processed")

def process_policy_data():
    """
    Pick the newest raw file (XML or dummy JSON),
    extract each item, classify as GDPR/CCPA/Other,
    and write cleaned CSV to data/processed.
    """
    # ensure output folder exists
    os.makedirs(PROCESSED_DIR, exist_ok=True)

    # find latest file
    files = sorted(glob.glob(os.path.join(RAW_DIR, "*")))
    latest = files[-1]
    print(f"Processing raw file: {latest}")

    raw_bytes = open(latest, "rb").read()
    text = raw_bytes.lstrip()

    items = []
    # JSON dummy?
    if text.startswith(b"{"):
        data = json.loads(raw_bytes)
        for entry in data.get("policies", []):
            items.append({
                "title": entry.get("title"),
                "link": entry.get("link", ""),
                "pubDate": entry.get("date"),
                "source": entry.get("source")
            })
    else:
        # parse RSS XML
        tree = ET.fromstring(raw_bytes)
        channel = tree.find("channel")
        for elem in channel.findall("item"):
            title   = elem.findtext("title", default="")
            link    = elem.findtext("link", default="")
            pubDate = elem.findtext("pubDate", default="")
            cats    = [c.text.upper() for c in elem.findall("category")]
            # simple classification
            if any("CCPA" in c for c in cats):
                source = "CCPA"
            elif any("GDPR" in c for c in cats):
                source = "GDPR"
            else:
                source = "Other"
            items.append({
                "title": title,
                "link": link,
                "pubDate": pubDate,
                "source": source
            })

    # write to CSV
    out_path = os.path.join(PROCESSED_DIR, "cleaned_policies.csv")
    with open(out_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["title", "link", "pubDate", "source"])
        writer.writeheader()
        writer.writerows(items)

    print(f"Wrote processed data to {out_path}")

if __name__ == "__main__":
    process_policy_data()

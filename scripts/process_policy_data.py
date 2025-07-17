# scripts/process_policy_data.py

import os
import glob
import json
import pandas as pd

from bs4 import BeautifulSoup  # if you ever need XML support


def process_policy_data():
    """
    Read raw JSON policy updates from data/raw, transform into a flat table,
    and write to data/processed/cleaned_policies.csv
    """
    # Define directories
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    processed_dir = os.path.join(base_dir, 'data', 'processed')
    os.makedirs(processed_dir, exist_ok=True)

    records = []

    # Load JSON files
    json_files = glob.glob(os.path.join(raw_dir, '*.json'))
    for jf in json_files:
        try:
            with open(jf, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[ERROR] Could not parse JSON file {jf}: {e}")
            continue

        # Each JSON file is expected to be a list of dicts
        for item in data:
            records.append({
                'source': 'EDPB',
                'title': item.get('title'),
                'link': item.get('link'),
                'date': item.get('date')
            })

    if not records:
        print("No policy records found.")
        return

    # Convert to DataFrame and save
    df = pd.DataFrame(records)
    out_path = os.path.join(processed_dir, 'cleaned_policies.csv')
    df.to_csv(out_path, index=False)
    print(f"Wrote processed data to {out_path}")


if __name__ == '__main__':
    process_policy_data()

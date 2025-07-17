import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import json

def parse_policy_xml(xml_file):
    """
    Parses a single XML file and returns a list of policy records as dictionaries.
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        records = []
        for policy in root.findall(".//policy"):
            record = {
                "id": policy.findtext("id"),
                "jurisdiction": policy.findtext("jurisdiction"),
                "title": policy.findtext("title"),
                "description": policy.findtext("description"),
                "issued_date": policy.findtext("issued_date"),
                "source": policy.findtext("source")
            }
            records.append(record)

        return records
    except Exception as e:
        print(f"[ERROR] Failed to parse {xml_file}: {e}")
        return []

def main():
    raw_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/raw"))
    processed_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/processed"))
    airflow_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../airflow_home/data"))

    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(airflow_data_dir, exist_ok=True)

    all_records = []

    for xml_file in glob.glob(os.path.join(raw_dir, "*.xml")):
        print(f"Processing raw file: {xml_file}")
        records = parse_policy_xml(xml_file)
        all_records.extend(records)

    if not all_records:
        print("No policy records found.")
        return

    df = pd.DataFrame(all_records)

    # Write to CSV
    csv_path = os.path.join(processed_dir, "cleaned_policies.csv")
    df.to_csv(csv_path, index=False)
    print(f"Wrote processed data to {csv_path}")

    # Write to JSON for downstream Airflow task
    json_path = os.path.join(airflow_data_dir, "processed_policy_data.json")
    with open(json_path, "w") as f:
        json.dump(df.to_dict(orient="records"), f, indent=2)
    print(f"Wrote JSON for Airflow to {json_path}")

if __name__ == "__main__":
    main()

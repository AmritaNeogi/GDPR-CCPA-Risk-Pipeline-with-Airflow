import os
import xml.etree.ElementTree as ET

def validate_latest_xml():
    raw_dir = "data/raw"
    files = sorted([
        os.path.join(raw_dir, f) for f in os.listdir(raw_dir)
        if f.endswith(".xml")
    ], reverse=True)

    if not files:
        print("❌ No XML files found in data/raw.")
        return

    latest_file = files[0]
    print(f"🔍 Validating: {latest_file}")
    try:
        tree = ET.parse(latest_file)
        root = tree.getroot()
        for policy in root.findall("policy"):
            title = policy.find("title").text
            date = policy.find("date").text
            print(f"📰 {date} — {title}")
    except Exception as e:
        print(f"❌ XML parsing failed: {e}")

if __name__ == "__main__":
    validate_latest_xml()

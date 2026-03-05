import csv
import json

schemes = []

with open("updated_data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        scheme = {
            "scheme_name": row.get("scheme_name", ""),
            "details": row.get("details", ""),
            "benefits": row.get("benefits", ""),
            "eligibility": row.get("eligibility", ""),
            "application_process": row.get("application", "")
        }

        schemes.append(scheme)

with open("myschemes_scraped.json", "w", encoding="utf-8") as f:
    json.dump(schemes, f, indent=2, ensure_ascii=False)

print("Converted successfully")

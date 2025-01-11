# src/updater.py
from .fetch_nist import fetch_nist_data
from .parser import parse_nvd_item
from .database import insert_or_update_vulnerability


def update_database():
    print("Starting database update...")
    nvd_items = fetch_nist_data()
    count_java = 0

    for item in nvd_items:
        parsed = parse_nvd_item(item)
        if parsed:
            insert_or_update_vulnerability(parsed)
            count_java += 1

    print(
        f"Database update completed! Inserted/updated {count_java} Oracle Java/GraalVM CVEs."
    )

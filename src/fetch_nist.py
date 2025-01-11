# src/fetch_nist.py
import os
import gzip
import requests
import json
from typing import List, Dict

BASE_URL = "https://nvd.nist.gov/feeds/json/cve/1.1"


def fetch_nist_data() -> List[Dict]:
    """
    Fetch and decompress the 2023 and 2024 NVD JSON files.
    Return a list of parsed CVE items (Python dictionaries).
    """
    cve_items = []
    years = ["2023", "2024"]

    for year in years:
        file_name = f"nvdcve-1.1-{year}.json.gz"
        url = f"{BASE_URL}/{file_name}"
        print(f"Fetching NVD feed for year {year} from {url} ...")

        # 1. Download the .gz file
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        with open(file_name, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        # 2. Decompress
        print(f"Finished downloading {file_name}. Decompressing now...")
        with gzip.open(file_name, "rt", encoding="utf-8") as gz:
            data = json.load(gz)
            items = data.get("CVE_Items", [])
            cve_items.extend(items)

        # Optional: remove the file
        if os.path.exists(file_name):
            os.remove(file_name)

    return cve_items

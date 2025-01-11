import re
import json


def parse_nvd_item(nvd_item: dict) -> dict:
    cve_id = nvd_item["cve"]["CVE_data_meta"]["ID"]
    desc_data = nvd_item["cve"]["description"].get("description_data", [])
    if not desc_data:
        return {}

    english_desc = ""
    for d in desc_data:
        if d.get("lang") == "en":
            english_desc = d.get("value", "").strip()
            break

    lower_desc = english_desc.lower()
    # Basic check for "oracle java se" or "graalvm"
    # to exclude random references to "java" or "javascript"
    if not any(
        kw in lower_desc for kw in ["oracle java se", "graalvm", "oracle graalvm"]
    ):
        return {}

    # Exclude if it mentions "javascript" only:
    if "javascript" in lower_desc:
        return {}

    # Extract short name
    short_name = extract_short_name(english_desc)

    # Extract version ranges and store as JSON
    version_json = extract_structured_versions(english_desc)

    # If we ended up with an empty version listing, you can decide whether to skip or not
    # For example:
    # if not version_json:
    #     return {}

    return {
        "cve_id": cve_id,
        "package_name": short_name,
        "vulnerable_versions": version_json,
    }


def extract_short_name(description_text: str) -> str:
    # Example cleanup
    # 1) Break at first period/semicolon
    parts = re.split(r"[.;]", description_text, 1)
    sentence = parts[0].strip()
    # 2) Remove leading "Vulnerability in the " if present
    sentence = re.sub(r"(?i)^vulnerability in the\s+", "", sentence)
    return sentence


def extract_structured_versions(description_text: str) -> str:
    # 1) Find text after "Supported versions that are affected are ..."
    match = re.search(
        r"(?i)supported\s+versions\s+that\s+are\s+affected\s+are\s+(.*)",
        description_text,
    )
    if not match:
        return ""

    raw_versions = match.group(1)
    # Optionally, cut off at "Difficult to exploit vulnerability" or similar phrases:
    for kw in [
        "Difficult to exploit vulnerability",
        "Successful attacks of this vulnerability",
    ]:
        idx = raw_versions.find(kw)
        if idx != -1:
            raw_versions = raw_versions[:idx]
            break

    # 2) Split by semicolons to separate product lines
    product_lines = [s.strip() for s in raw_versions.split(";") if s.strip()]
    structured = {}
    for line in product_lines:
        if ":" in line:
            prod, vers = line.split(":", 1)
            prod = prod.strip()
            versions_list = [v.strip() for v in vers.split(",")]
            structured[prod] = versions_list
        else:
            # If there's no colon, just store the entire line
            structured[line] = []

    return json.dumps(structured)

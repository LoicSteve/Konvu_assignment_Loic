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
    # Basic check for Oracle Java SE / GraalVM references,
    # now also explicitly includes "oracle graalvm for jdk".
    if not any(
        kw in lower_desc
        for kw in [
            "oracle java se",
            "oracle graalvm",
            "oracle graalvm for jdk"
        ]
    ):
        return {}

    # Exclude if it only mentions "javascript" (to avoid false positives)
    if "javascript" in lower_desc:
        return {}

    # Extract short name
    short_name = extract_short_name(english_desc)

    # Extract version ranges as JSON
    version_json = extract_structured_versions(english_desc)

    return {
        "cve_id": cve_id,
        "package_name": short_name,
        "vulnerable_versions": version_json,
    }


def extract_short_name(description_text: str) -> str:
    # 1) Break at the first period or semicolon
    parts = re.split(r"[.;]", description_text, maxsplit=1)
    sentence = parts[0].strip()
    # 2) Remove leading "Vulnerability in the " if present
    sentence = re.sub(r"(?i)^vulnerability in the\s+", "", sentence)
    return sentence


def extract_structured_versions(description_text: str) -> str:
    """
    Find everything after "Supported versions that are affected are"
    and parse each product line separated by semicolons, storing
    them as a JSON-encoded dictionary.
    """
    match = re.search(
        r"(?i)supported\s+versions\s+that\s+are\s+affected\s+are\s+(.*)",
        description_text,
    )
    if not match:
        return ""

    raw_versions = match.group(1)

    # Optionally cut off at key phrases
    for kw in [
        "Difficult to exploit vulnerability",
        "Successful attacks of this vulnerability",
    ]:
        idx = raw_versions.find(kw)
        if idx != -1:
            raw_versions = raw_versions[:idx]
            break

    # Split by semicolons to separate product lines, e.g.:
    # "Oracle Java SE: 8u391, 11.0.21; Oracle GraalVM for JDK: 17.0.9"
    product_lines = [s.strip() for s in raw_versions.split(";") if s.strip()]

    structured = {}
    for line in product_lines:
        if ":" in line:
            prod, vers = line.split(":", 1)
            prod = prod.strip()
            versions_list = [v.strip() for v in vers.split(",")]
            structured[prod] = versions_list
        else:
            structured[line] = []

    return json.dumps(structured)

# tests/test_fetch_nist.py
import os
import json
import gzip
import io
from unittest.mock import patch, MagicMock

from src.fetch_nist import fetch_nist_data


@patch("src.fetch_nist.requests.get")
def test_fetch_nist_data(mock_get, tmp_path):
    """
    Test fetch_nist_data() by mocking the requests.get call so we don't do a real download.
    We'll simulate returning a compressed JSON file for a single year.
    """
    # 1) Build a mock JSON structure
    mock_json_data = {
        "CVE_Items": [
            {
                "cve": {
                    "CVE_data_meta": {"ID": "CVE-2024-0001"},
                    "description": {
                        "description_data": [
                            {"lang": "en", "value": "Test vulnerability for 2024."}
                        ]
                    },
                }
            }
        ]
    }
    encoded_json = json.dumps(mock_json_data).encode("utf-8")

    # 2) Compress the JSON in memory, as if it were .gz
    gz_buffer = io.BytesIO()
    with gzip.GzipFile(fileobj=gz_buffer, mode="wb") as gz_file:
        gz_file.write(encoded_json)
    gz_bytes = gz_buffer.getvalue()

    # 3) Mock the response from requests.get
    mock_response = MagicMock()
    mock_response.iter_content = lambda chunk_size: [gz_bytes]
    mock_response.raise_for_status = MagicMock()
    mock_response.status_code = 200

    # Each time we call requests.get, return this mock response
    mock_get.return_value = mock_response

    # 4) Now call fetch_nist_data() - it should do everything in memory
    cve_items = fetch_nist_data()  # This normally downloads 2023, 2024, etc.

    # 5) Assertions
    # We expect that cve_items will contain 2 items
    assert len(cve_items) == 2
    assert cve_items[0]["cve"]["CVE_data_meta"]["ID"] == "CVE-2024-0001"
    assert (
        "Test vulnerability for 2024."
        in cve_items[0]["cve"]["description"]["description_data"][0]["value"]
    )

    # Check that requests.get was called for 2023 and 2024 feeds
    # Because in your fetch_nist_data, you likely do something like:
    # years = ["2023", "2024"]
    expected_calls = [
        ("https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-2023.json.gz",),
        ("https://nvd.nist.gov/feeds/json/cve/1.1/nvdcve-1.1-2024.json.gz",),
    ]
    actual_calls = [call.args for call in mock_get.call_args_list]
    assert actual_calls == expected_calls

    # If your code removes them, you can verify they don't exist in the current directory
    for year in ["2023", "2024"]:
        gz_name = f"nvdcve-1.1-{year}.json.gz"
        assert not os.path.exists(gz_name), f"File {gz_name} should have been removed."

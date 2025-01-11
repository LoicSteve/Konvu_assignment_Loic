# tests/test_updater.py
from unittest.mock import patch
from src.updater import update_database
from src.database import initialize_db
import os


@patch("src.updater.fetch_nist_data")
@patch("src.updater.parse_nvd_item")
@patch("src.updater.insert_or_update_vulnerability")
def test_update_database(
    mock_insert_or_update, mock_parse_nvd_item, mock_fetch_nist_data, tmp_path
):
    """
    Test that update_database() loops over the items from fetch_nist_data,
    calls parse_nvd_item, and if parsed_data is not empty, calls insert_or_update_vulnerability.
    """
    # 1) Mock fetch_nist_data to return 2 raw items
    mock_fetch_nist_data.return_value = [
        {"cve": {"CVE_data_meta": {"ID": "CVE-2024-0001"}}, "some_key": "value"},
        {"cve": {"CVE_data_meta": {"ID": "CVE-2024-0002"}}, "some_key": "value"},
    ]

    # 2) Mock parse_nvd_item to return a dict for the first item, {} for the second
    # This simulates that the second item isn't recognized as a Java vuln
    mock_parse_nvd_item.side_effect = [
        {
            "cve_id": "CVE-2024-0001",
            "package_name": "some_package",
            "vulnerable_versions": "",
        },
        {},
    ]

    # 3) Initialize a test DB in a temp folder (optional)
    test_db = str(tmp_path / "test_vulnerabilities.db")
    os.environ["TEST_DB_PATH"] = test_db  # if your code references an env or something

    initialize_db()  # This ensures the schema is created in the current directory if that's how you do it

    # 4) Call the function under test
    update_database()

    # 5) Assertions
    # fetch_nist_data was called once
    mock_fetch_nist_data.assert_called_once()

    # parse_nvd_item was called for each item in the mock_fetch_nist_data list
    assert mock_parse_nvd_item.call_count == 2

    # insert_or_update_vulnerability should be called only once (the first item returned a dict, second returned {})
    mock_insert_or_update.assert_called_once()
    (arg1,), _ = mock_insert_or_update.call_args
    assert arg1["cve_id"] == "CVE-2024-0001"
    assert arg1["package_name"] == "some_package"

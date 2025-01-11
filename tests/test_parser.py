from src.parser import parse_nvd_item


def test_parse_nvd_item_oracle_java():
    """
    Check that parse_nvd_item correctly identifies a CVE with Oracle Java SE / GraalVM
    in the description and extracts the right fields.
    """
    # Create a mock NVD item
    mock_item = {
        "cve": {
            "CVE_data_meta": {"ID": "CVE-2024-99999"},
            "description": {
                "description_data": [
                    {
                        "lang": "en",
                        "value": "Vulnerability in the Oracle Java SE, Oracle GraalVM for JDK... "
                        "Supported versions that are affected are Oracle Java SE: 8u391, 17.0.9;"
                        " Oracle GraalVM for JDK: 17.0.9, 21.0.1. Difficult to exploit vulnerability...",
                    }
                ]
            },
        }
    }

    result = parse_nvd_item(mock_item)

    # We expect parse_nvd_item to return a dictionary with certain keys
    assert result["cve_id"] == "CVE-2024-99999"
    assert (
        "Oracle Java SE" in result["package_name"]
    )  # or however you define the short name
    assert "8u391" in result["vulnerable_versions"]  # check version extraction
    assert (
        "17.0.9" in result["vulnerable_versions"]
    )  # check it parsed multiple versions


def test_parse_nvd_item_not_java():
    """
    Check that parse_nvd_item returns an empty dict for CVE descriptions
    that do not mention Oracle Java or GraalVM.
    """
    mock_item = {
        "cve": {
            "CVE_data_meta": {"ID": "CVE-2024-00001"},
            "description": {
                "description_data": [
                    {
                        "lang": "en",
                        "value": "A vulnerability in a random piece of software that is not Java related.",
                    }
                ]
            },
        }
    }

    result = parse_nvd_item(mock_item)
    assert result == {}, "Expected an empty dict for non-Java vulnerabilities"


def test_parse_nvd_item_javascript_confusion():
    """
    Ensure that we skip or properly exclude items mentioning 'JavaScript' but not actual 'Oracle Java SE'.
    """
    mock_item = {
        "cve": {
            "CVE_data_meta": {"ID": "CVE-2024-00002"},
            "description": {
                "description_data": [
                    {
                        "lang": "en",
                        "value": "This CVE mentions JavaScript for XSS but not Oracle Java SE.",
                    }
                ]
            },
        }
    }

    result = parse_nvd_item(mock_item)
    assert (
        result == {}
    ), "Should exclude JavaScript references that aren't real Java vulnerabilities."

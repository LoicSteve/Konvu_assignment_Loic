# tests/test_database.py
import pytest
import sqlite3
from src.database import initialize_db, insert_or_update_vulnerability, DB_FILE


@pytest.fixture
def setup_test_db(tmp_path):
    """
    Use a temporary directory for the database file to avoid
    overwriting the real vulnerabilities.db.
    """
    test_db_path = tmp_path / "test_vulnerabilities.db"
    # Overwrite the DB_FILE reference for testing (hacky but quick).
    original_db_file = DB_FILE
    from src import database

    database.DB_FILE = str(test_db_path)

    yield  # run the test

    # teardown - revert DB_FILE
    database.DB_FILE = original_db_file


def test_database_insert_update(setup_test_db):
    """
    Test inserting and updating a vulnerability record in our database.
    """
    # 1. Initialize DB
    initialize_db()

    # 2. Insert a mock record
    mock_data = {
        "cve_id": "CVE-2024-ABCDE",
        "package_name": "Oracle Java SE (Hotspot)",
        "vulnerable_versions": "Oracle Java SE: 8u391",
    }
    insert_or_update_vulnerability(mock_data)

    # 3. Read back from the DB to confirm
    from src.database import DB_FILE

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT cve_id, package_name, vulnerable_versions FROM vulnerabilities"
    )
    rows = cursor.fetchall()
    conn.close()

    assert len(rows) == 1, "Should have exactly one record in the DB"
    assert rows[0] == (
        "CVE-2024-ABCDE",
        "Oracle Java SE (Hotspot)",
        "Oracle Java SE: 8u391",
    )

    # 4. Update the same record
    updated_data = {
        "cve_id": "CVE-2024-ABCDE",
        "package_name": "Oracle Java SE Updated",
        "vulnerable_versions": "Oracle Java SE: 8u400",
    }
    insert_or_update_vulnerability(updated_data)

    # Re-check
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT cve_id, package_name, vulnerable_versions FROM vulnerabilities"
    )
    rows = cursor.fetchall()
    conn.close()

    assert len(rows) == 1, "Should still have exactly one record (updated in place)"
    assert rows[0] == (
        "CVE-2024-ABCDE",
        "Oracle Java SE Updated",
        "Oracle Java SE: 8u400",
    )

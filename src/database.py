# src/database.py
import sqlite3
from typing import Dict

DB_FILE = "vulnerabilities.db"


def initialize_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # We remove 'description TEXT' from the schema
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS vulnerabilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cve_id TEXT NOT NULL UNIQUE,
            package_name TEXT NOT NULL,
            vulnerable_versions TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_vulnerabilities_cve
        ON vulnerabilities (cve_id)
    """
    )

    conn.commit()
    conn.close()


def insert_or_update_vulnerability(vuln_data: Dict):
    """
    Insert or update a vulnerability row based on cve_id.
    We'll skip if vuln_data is empty (parser returned nothing).
    """
    if not vuln_data or "cve_id" not in vuln_data:
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 'description' is removed; only these columns remain:
    cursor.execute(
        """
        INSERT INTO vulnerabilities (
            cve_id, package_name, vulnerable_versions
        )
        VALUES (?, ?, ?)
        ON CONFLICT(cve_id) DO UPDATE SET
            package_name = excluded.package_name,
            vulnerable_versions = excluded.vulnerable_versions
    """,
        (
            vuln_data["cve_id"],
            vuln_data["package_name"],
            vuln_data.get("vulnerable_versions", ""),
        ),
    )
    conn.commit()
    conn.close()

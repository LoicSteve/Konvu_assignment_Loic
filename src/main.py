# src/main.py
import sys
from .database import initialize_db
from .updater import update_database


def main():
    initialize_db()
    update_database()


if __name__ == "__main__":
    sys.exit(main())

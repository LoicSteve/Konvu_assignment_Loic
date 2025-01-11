# Konvu_assignment_Loic


[![CI](https://github.com/LoicSteve/Konvu_assignment_Loic/actions/workflows/main.yml/badge.svg)](https://github.com/LoicSteve/Konvu_assignment_Loic/actions/workflows/main.yml)
---

# Konvu Java Vulnerability Database

**A Python-based solution to fetch, parse, and store Java-related CVE data from the NIST (NVD) feeds, with a streamlined workflow for testing, linting, and containerization.**

---

## Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Project Structure](#project-structure)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [Testing](#testing)  
7. [Linting & Formatting](#linting--formatting)  
8. [Dockerization](#dockerization)  
9. [Rationale](#rationale)  
10. [AI Tools & Assistance](#ai-tools--assistance)  
11. [Future Improvements](#future-improvements)  
12. [License](#license)

---

## Overview
This project aims to **detect and track Java-specific vulnerabilities** by analyzing the [NIST (NVD) JSON feeds](https://nvd.nist.gov/vuln/data-feeds#JSON_FEED) for **2023 and 2024**.  
We focus on:
- Identifying **Java** (Oracle Java SE, GraalVM, etc.) vulnerabilities from large sets of CVE data.  
- Storing them in a simple, local **SQLite** database (`vulnerabilities.db`).  
- Offering a clean pipeline (via **Makefile** and **Docker**) for an efficient developer experience.

---

## Features
- **Automated Feed Download**: Grabs and decompresses `.gz` feeds for 2023/2024.  
- **Parsing Logic**: Identifies Java vulnerabilities using textual patterns in CVE descriptions.  
- **SQLite Storage**: Maintains a local DB with key fields (CVE ID, package name, version info, etc.).  
- **Testing & Coverage**: Uses `pytest` (+ `pytest-cov`) to validate correctness.  
- **Formatting & Linting**: `black` for code formatting, `pylint` for static analysis.  
- **Makefile** Automations: Simple commands (`make install`, `make test`, `make lint`, `make run`, etc.).  
- **Dockerized**: Easily spin up a container with the entire environment pre-configured.

---

## Project Structure

```
Konvu_assignment/
├── Dockerfile
├── Makefile
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── fetch_nist.py
│   ├── parser.py
│   ├── updater.py
│   └── main.py
├── tests/
│   ├── test_database.py
│   ├── test_fetch_nist.py
│   ├── test_parser.py
│   └── test_updater.py
└── vulnerabilities.db  (created at runtime)
```

**Key directories**:
- **`src/`**: Application code (database logic, fetching, parsing, updating).  
- **`tests/`**: Unit tests for parser, database, fetching, etc.  
- **`vulnerabilities.db`**: SQLite database generated after the program is run.

---

## Installation

1. **Clone** the repository or download the ZIP:
   ```bash
   git clone https://github.com/your-username/konvu_assignment.git
   cd konvu_assignment
   ```

2. **(Optional) Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/Mac
   # or
   venv\Scripts\activate.bat  # Windows
   ```

3. **Install dependencies** using the **Makefile**:
   ```bash
   make install
   ```
   This upgrades `pip` and installs everything in `requirements.txt` (including `pytest`, `pylint`, `black`, etc.).

---

## Usage

### **1. Run**  
To **download, parse, and store** the vulnerabilities in `vulnerabilities.db`, simply:

```bash
make run
```
This executes `python -m src.main` under the hood, which:
- Fetches **2023** and **2024** JSON feeds from NVD,  
- Extracts **Java**-related vulnerabilities,  
- Saves them into `vulnerabilities.db`.

### **2. Querying the Database**  
If you have `sqlite3` installed locally (or inside Docker with `apt-get install sqlite3`), you can inspect:

```bash
sqlite3 vulnerabilities.db
sqlite> .tables
sqlite> SELECT * FROM vulnerabilities LIMIT 5;
```

---

## Testing

All tests live in the **`tests/`** folder. We use **`pytest`** (plus `pytest-cov` for coverage).  
To run tests with coverage:

```bash
make test
```

Under the hood, this runs:
```bash
pytest --maxfail=1 --disable-warnings -vv \
       --cov=src --cov=./tests --cov-report=term-missing ./tests
```

---

## Linting & Formatting

1. **Lint**  
   ```bash
   make lint
   ```
   Uses **pylint** to analyze code quality in `src/` and `tests/`.

2. **Format**  
   ```bash
   make format
   ```
   Runs **black** on `src/` and `tests/` for consistent code style.

---

## Dockerization

A **Dockerfile** is included to containerize everything. Steps:

1. **Build** the image:
   ```bash
   docker build -t konvu_assignment:latest .
   ```
2. **Run** an interactive shell:
   ```bash
   docker run -it --rm konvu_assignment:latest
   ```
   Inside the container:
   ```bash
   # Install, test, run, etc.
   make install
   make test
   make run
   ```

This ensures everyone on your team (and your CI/CD) uses the **same** Python environment with consistent dependencies.

---

## Rationale

- **Python** chosen for its wide library support (`requests`, `pytest`, `sqlite3`, etc.) and readability.  
- **SQLite** as a simple, file-based database—no extra server to manage.  
- **`requests.get(..., stream=True)`** to handle large `.gz` feeds.  
- **`pytest` + `pytest-cov`** for robust, measurable testing.  
- **`pylint` + `black`** for code consistency and clarity.  
- **Docker** for reproducibility across dev machines and CI.

---

## AI Tools & Assistance

In the development process, AI tools like **ChatGPT** were used to:
- Brainstorm the **project structure**  
- Suggest **regex patterns** for detecting Java references in the CVE description  
- Provide **examples** of parsing large JSON feeds  
- Generate **Makefile** stubs for test, lint, and run tasks  
- Offer code reviews and refinement suggestions

All code has been **reviewed** and **modified** by the project maintainers to ensure accuracy and maintainability.

---

## Future Improvements

1. **Incremental Feeds**: Instead of downloading entire years, parse the “modified” or “recent” feeds for more efficient updates.  
2. **Streaming JSON Parser**: Use [ijson](https://pypi.org/project/ijson/) to handle large NVD data in a memory-friendly way.  
3. **OSV Integration**: Optionally query [OSV.dev](https://osv.dev) for extended vulnerability details.  
4. **Auto-Detection**: More advanced **regex** or machine-learning to reliably classify Java vulnerabilities.  
5. **CI Pipeline**: Integrate GitHub Actions or another CI to automatically run tests, lint, and build Docker images on each commit.

---


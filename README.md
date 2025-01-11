# Konvu Java Vulnerability Database 
[![CI](https://github.com/LoicSteve/Konvu_assignment_Loic/actions/workflows/main.yml/badge.svg)](https://github.com/LoicSteve/Konvu_assignment_Loic/actions/workflows/main.yml)


**A Python-based solution to fetch, parse, and store Java-related CVE data from the NIST (NVD) feeds, with a streamlined workflow for testing, linting, containerization, and continuous integration.**

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
10. [CI Pipeline](#ci-pipeline)  
11. [AI Tools & Assistance](#ai-tools--assistance)  
12. [Future Improvements](#future-improvements)  

---

## Overview
This project aims to **detect and track Java-specific vulnerabilities** by analyzing the [NIST (NVD) JSON feeds](https://nvd.nist.gov/vuln/data-feeds#JSON_FEED) for **2023 and 2024**.  
We focus on:
- Identifying **Java** (Oracle Java SE, GraalVM, etc.) vulnerabilities from large sets of CVE data.  
- Storing them in a simple, local **SQLite** database (`vulnerabilities.db`).  
- Offering a clean pipeline (via **Makefile**, **Docker**, and **CI**) for an efficient developer experience.

---

## Features
- **Automated Feed Download**: Grabs and decompresses `.gz` feeds for 2023/2024.  
- **Parsing Logic**: Identifies Java vulnerabilities using textual patterns in CVE descriptions.  
- **SQLite Storage**: Maintains a local DB with key fields (CVE ID, package name, version info).  
- **Testing & Coverage**: Uses `pytest` (+ `pytest-cov`) to validate correctness.  
- **Formatting & Linting**: `black` for code formatting, `pylint` for static analysis.  
- **Makefile** Automation: Simple commands (`make install`, `make lint`, `make test`, `make run`, etc.).  
- **Dockerized**: Easily spin up a container with the entire environment pre-configured.  
- **Integrated CI Pipeline**: GitHub Actions workflow to run tests and checks on every push.

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
├── .github/
│   └── workflows/
│       └── main.yml   (GitHub Actions CI workflow)
└── vulnerabilities.db  (created at runtime)
```

**Key directories**:
- **`src/`**: Application code (database logic, fetching, parsing, updating).  
- **`tests/`**: Unit tests for parser, database, fetching, etc.  
- **`.github/workflows`**: Configuration for the GitHub Actions CI pipeline.  
- **`vulnerabilities.db`**: SQLite database file, generated after the program is run.

---

## Installation

1. **Clone** the repository or download the ZIP:
   ```bash
   git clone https://github.com/LoicSteve/Konvu_assignment_Loic.git
   cd Konvu_assignment_Loic
   ```

2. **(Optional) Create a virtual environment**:
   ```bash
   python3 -m venv venv   # In my case konvu
   source venv/bin/activate   # Linux/Mac
   # or
   venv\Scripts\activate.bat  # Windows
   ```

3. **Install dependencies** using the **Makefile**:
   ```bash
   make install
   ```
   This command upgrades `pip` and installs everything in `requirements.txt` (including `pytest`, `pylint`, `black`, etc.).

---

## Usage

### **1. Run**  
To **download, parse, and store** the vulnerabilities in `vulnerabilities.db`:

```bash
make run
```
This executes `python -m src.main` under the hood, which:
- Fetches **2023** and **2024** JSON feeds from NVD,  
- Extracts **Java**-related vulnerabilities,  
- Saves them into `vulnerabilities.db`.

### **2. Querying the Database**  
If you have `sqlite3` installed:

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

Under the hood, this runs something like:
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

This ensures consistent environment across machines and CI.

---

## Rationale

- **Python** for its ecosystem and readability.  
- **SQLite** for a simple, file-based database—no additional server needed.  
- **Pytest + Pytest-cov** for robust testing and coverage metrics.  
- **Black + Pylint** for standardized formatting and linting.  
- **Docker** for reproducible dev & production.  
- **GitHub Actions** for continuous integration, ensuring code quality checks on every push.

---

## CI Pipeline

This repository leverages **GitHub Actions** to **automatically**:
1. Install dependencies,  
2. Run lint checks,  
3. Execute the test suite,  
4. (Optionally) build and push Docker images or gather coverage artifacts.

The current status of the pipeline is shown by the badge below:

[![CI](https://github.com/LoicSteve/Konvu_assignment_Loic/actions/workflows/main.yml/badge.svg)](https://github.com/LoicSteve/Konvu_assignment_Loic/actions/workflows/main.yml)

---

## AI Tools & Assistance

In the development process, AI tools (like **ChatGPT**) were used to:
- Brainstorm **project structure** and code design.  
- Suggest **regex** patterns and parsing logic for CVEs.  
- Generate **Dockerfile**/**Makefile** stubs.  
- Provide code reviews and improvement ideas.

All code has been reviewed and refined by the project maintainers to ensure accuracy and maintainability.

---

## Future Improvements

1. **Incremental Feeds**: Instead of downloading entire years, parse the “modified” or “recent” feeds for more efficient updates.  
2. **Streaming JSON Parser**: Use [ijson](https://pypi.org/project/ijson/) to handle large NVD data in a memory-friendly way.  
3. **OSV Integration**: Optionally query [OSV.dev](https://osv.dev) for extended vulnerability details.  
4. **Advanced Detection**: Smarter regex or ML-based classification to reliably identify Java vulnerabilities.  

---



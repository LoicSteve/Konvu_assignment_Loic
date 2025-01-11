# Makefile

# --------------------------------------------------------------------------------
# VARIABLES
# --------------------------------------------------------------------------------

PROJECT_NAME := "Konvu_assignment"
PYTHON := python
PIP := pip

# Directory containing tests
TEST_DIR := ./tests

# --------------------------------------------------------------------------------
# TARGETS
# --------------------------------------------------------------------------------

# INSTALL
install:
	@echo "Installing dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# TEST
test:
	@echo "Running tests with coverage..."
	$(PYTHON) -m pytest --maxfail=1 --disable-warnings -vv \
		--cov=src --cov=$(TEST_DIR) --cov-report=term-missing $(TEST_DIR)


# FORMAT
format:
	@echo "Running Black formatter..."
	black src tests

# LINT
lint:
	@echo "Running pylint..."
	pylint src tests \
		--disable=R,C,W0621,W0613,W0404
# RUN
run:
	@echo "Running the main program..."
	$(PYTHON) -m src.main

# ALL
all: install lint test format

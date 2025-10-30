# Allowed box drawing characters for visual output
ALLOWED_BOX_CHARS := "├\|│\|└\|┌\|┐\|┘\|┴\|┬\|┤\|┼"

# Python virtual environment directories to exclude
VENV_DIRS := --exclude-dir=venv --exclude-dir=.venv --exclude-dir=env --exclude-dir=.env

# Exclude files with intentional multi-language content
EXCLUDE_FILES := --exclude=prompts.py

# Python path
PYTHON := .venv/bin/python
PIP := .venv/bin/pip
RUFF := .venv/bin/ruff
MYPY := .venv/bin/mypy

# Target directory for linting (backend code)
BACKEND_DIR := backend

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make lint          - Run all linters (English check + ruff + mypy)"
	@echo "  make check-english - Check for non-English characters in code"
	@echo "  make ruff          - Run ruff linter"
	@echo "  make ruff-fix      - Run ruff with auto-fix"
	@echo "  make mypy          - Run mypy type checker"
	@echo "  make format        - Format code with ruff"
	@echo "  make install       - Install linting dependencies"

# Main lint target - runs all checks
.PHONY: lint
lint: check-english ruff mypy

# Check for non-English characters in comments and docstrings
.PHONY: check-english
check-english:
	@echo "Checking for non-English characters in comments..."
	@if LC_ALL=C grep -rn "#.*[^	 !-~]" $(BACKEND_DIR) --include="*.py" $(VENV_DIRS) $(EXCLUDE_FILES) | grep -v $(ALLOWED_BOX_CHARS) | grep -q .; then \
		echo "ERROR: Found non-English characters in comments:"; \
		LC_ALL=C grep -rn "#.*[^	 !-~]" $(BACKEND_DIR) --include="*.py" $(VENV_DIRS) $(EXCLUDE_FILES) | grep -v $(ALLOWED_BOX_CHARS); \
		exit 1; \
	fi
	@echo "Checking for non-English characters in docstrings..."
	@if LC_ALL=C grep -rn '""".*[^	 !-~]' $(BACKEND_DIR) --include="*.py" $(VENV_DIRS) $(EXCLUDE_FILES) | grep -v $(ALLOWED_BOX_CHARS) | grep -q .; then \
		echo "ERROR: Found non-English characters in docstrings:"; \
		LC_ALL=C grep -rn '""".*[^	 !-~]' $(BACKEND_DIR) --include="*.py" $(VENV_DIRS) $(EXCLUDE_FILES) | grep -v $(ALLOWED_BOX_CHARS); \
		exit 1; \
	fi
	@if LC_ALL=C grep -rn "'''.*[^	 !-~]" $(BACKEND_DIR) --include="*.py" $(VENV_DIRS) $(EXCLUDE_FILES) | grep -v $(ALLOWED_BOX_CHARS) | grep -q .; then \
		echo "ERROR: Found non-English characters in docstrings:"; \
		LC_ALL=C grep -rn "'''.*[^	 !-~]" $(BACKEND_DIR) --include="*.py" $(VENV_DIRS) $(EXCLUDE_FILES) | grep -v $(ALLOWED_BOX_CHARS); \
		exit 1; \
	fi
	@echo "✓ No non-English characters found"

# Run ruff linter
.PHONY: ruff
ruff:
	@echo "Running ruff linter..."
	$(RUFF) check $(BACKEND_DIR)

# Run ruff with auto-fix
.PHONY: ruff-fix
ruff-fix:
	@echo "Running ruff with auto-fix..."
	$(RUFF) check --fix $(BACKEND_DIR)

# Run mypy type checker
.PHONY: mypy
mypy:
	@echo "Running mypy type checker..."
	$(MYPY) $(BACKEND_DIR)

# Format code with ruff
.PHONY: format
format:
	@echo "Formatting code with ruff..."
	$(RUFF) format $(BACKEND_DIR)

# Install linting dependencies
.PHONY: install
install:
	@echo "Installing linting dependencies..."
	$(PIP) install ruff mypy
	@echo "✓ Linting tools installed"

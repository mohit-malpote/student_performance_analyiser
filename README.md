# Class Performance Analyzer 📊

[![CI Pipeline](https://github.com/mohit-malpote/student_performance_analyiser/actions/workflows/ci.yml/badge.svg)](https://github.com/mohit-malpote/student_performance_analyiser/actions/workflows/ci.yml)
[![Python Versions](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A Flask-based web application and database backend for analyzing classroom performance, tracking student assessments (Unit Tests, Semester Exams), and managing teacher-subject-class relationships.

---

## 🚀 Continuous Integration (CI) Pipeline

This project is configured with an automated **GitHub Actions CI Pipeline** (`.github/workflows/ci.yml`) that runs on every `push` and `pull_request` to `main`, as well as manual triggers (`workflow_dispatch`).

### Pipeline Stages

1. **Linting & Code Quality (`lint`)**:
   - Compiles Python files to ensure zero syntax errors (`py_compile`).
   - Runs `flake8` to enforce PEP 8 style guidelines.
2. **Matrix Automated Testing & Coverage (`test`)**:
   - Tests across multiple Python versions: **3.10, 3.11, 3.12, and 3.13**.
   - Runs the test suite via `pytest` with code coverage report (`pytest-cov`).
   - Validates the database seeding script (`seed_data.py`).
   - Generates and uploads coverage XML artifacts.
3. **Smoke Testing (`smoke-test`)**:
   - Validates that Flask application contexts (`app.py` and `Dummy_ERP/app.py`) initialize cleanly with SQLAlchemy.
4. **CI Status Aggregator (`ci-status`)**:
   - Provides a unified branch protection status check.

---

## 🛠️ Local Development Setup

### 1. Prerequisites
- Python 3.10 or higher
- Git

### 2. Clone Repository & Setup Virtual Environment
```bash
git clone https://github.com/mohit-malpote/student_performance_analyiser.git
cd class_performance_analysiser

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Linux / macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install runtime and development dependencies
pip install -r requirements-dev.txt
```

### 4. Seed the Database
```bash
python seed_data.py
```

### 5. Run the Application
```bash
# Run the main analyzer app:
python app.py

# Or run the Dummy ERP portal:
python Dummy_ERP/app.py
```

---

## 🧪 Running Tests & Linting Locally

Run the complete test suite and generate a coverage report:
```bash
pytest --cov=. --cov-report=term-missing
```

Run PEP 8 linting checks:
```bash
flake8
```

Verify Python syntax without executing:
```bash
python -m py_compile app.py models.py seed_data.py Dummy_ERP/app.py
```

---

## 📁 Project Structure

```
class_performance_analysiser/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI workflow
├── tests/                       # Automated test suite
│   ├── conftest.py              # Pytest fixtures and test DB setup
│   ├── test_app.py              # Main app endpoint tests
│   ├── test_dummy_erp.py        # Dummy ERP app and auth tests
│   ├── test_models.py           # Database model and relation tests
│   └── test_seed_data.py        # Database seeding tests
├── Dummy_ERP/                   # ERP demo portal
│   ├── app.py                   # ERP Flask application
│   └── templates/               # ERP HTML templates
├── app.py                       # Main application entry point
├── models.py                    # SQLAlchemy database models
├── seed_data.py                 # Database population script
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Dev, test & CI dependencies
├── .flake8                      # Flake8 configuration
├── pytest.ini                   # Pytest configuration
├── .gitignore                   # Git ignore patterns
└── README.md                    # Project documentation
```

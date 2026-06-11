# Enterprise API Automation Framework

Enterprise-grade Python API automation framework with scalable architecture, reporting, CI/CD, Docker support, retry mechanism, and modular utilities.

## Architecture

```
enterprise-api-framework/
├── app/                  # FastAPI mock server (for local testing)
├── config/
│   ├── default.env       # Committed default configuration
│   ├── dev.env           # Development overrides
│   ├── qa.env            # QA overrides (gitignored)
│   └── prod.env          # Production overrides (gitignored)
├── core/                 # Core framework
│   ├── api_client.py     # HTTP client (GET/POST/PUT/PATCH/DELETE)
│   ├── assertions.py     # Reusable assertion helpers
│   ├── config_manager.py # Environment-aware configuration loader
│   ├── logger.py         # Loguru logger with file rotation
│   ├── reporting.py      # Custom HTML dashboard generator
│   └── retry_handler.py  # Tenacity retry decorator
├── logs/                 # Runtime logs
├── models/
│   ├── request_models/   # Pydantic request schemas
│   └── response_models/  # Pydantic response schemas
├── reports/              # HTML, Dashboard and Allure reports
├── testdata/
│   ├── users.json        # User test data
│   └── payloads/         # API payload fixtures
├── tests/
│   ├── smoke/            # Smoke tests
│   ├── regression/       # Regression tests
│   └── integration/      # Integration tests (FakeStore, external APIs)
├── utils/
│   ├── helpers.py        # General utility helpers
│   ├── json_utils.py     # JSON read/write utilities
│   └── validators.py     # Reusable validation functions
├── .github/workflows/    # CI/CD pipelines
├── conftest.py           # Pytest fixtures & hooks
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── requirements.txt
└── README.md
```

## Features

- **API Client** with GET/POST/PUT/DELETE/PATCH methods and retry mechanism (tenacity) — DRY single `_request` method
- **Logging** via Loguru with rotation and retention
- **Response Validation** using Pydantic models
- **Custom Dashboard** auto-generated HTML report with pie chart, duration bars, and test details
- **Allure Reports** for rich test dashboards
- **Parallel Execution** with pytest-xdist
- **CI/CD** via GitHub Actions
- **Docker** containerization
- **Test Data Management** with JSON fixtures
- **FastAPI Mock Server** (`app/`) for local development and testing
- **Environment-aware config** — switch between dev/qa/prod via `APP_ENV` variable

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| pytest | Test runner |
| requests | HTTP client |
| Pydantic | Response validation |
| Loguru | Logging |
| Allure | Advanced reporting |
| pytest-xdist | Parallel execution |
| Tenacity | Retry mechanism |
| FastAPI | Mock server |
| Docker | Containerization |
| GitHub Actions | CI/CD |

## Installation

```bash
git clone <repo-url>
cd enterprise-api-framework
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

## Execution

```bash
# Run all tests
pytest

# Run with HTML report
pytest --html=reports/report.html

# Run with Allure
pytest --alluredir=reports/allure-results
allure serve reports/allure-results

# Run in parallel (4 workers)
pytest -n 4

# Run specific folder
pytest tests/smoke/
pytest tests/regression/
pytest tests/integration/
```

## Docker

```bash
docker build -t api-framework .
docker run api-framework

# Or use docker-compose
docker-compose up
```

## Mock Server

A FastAPI mock server is included in `app/` for local testing:

```bash
uvicorn app.main:app --reload
```

## CI/CD

Push to `master` branch triggers automatic test execution via GitHub Actions, with HTML, Dashboard, and Allure reports uploaded as artifacts.

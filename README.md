# Enterprise API Automation Framework

Enterprise-grade Python API automation framework with scalable architecture, reporting, CI/CD, Docker support, retry mechanism, and modular utilities.

## Architecture

```
enterprise-api-framework/
├── app/                  # FastAPI mock server (for local testing)
├── config/               # Environment configuration (.env)
├── logs/                 # Runtime logs
├── models/               # Pydantic response models
├── reports/              # HTML and Allure reports
├── testdata/             # JSON test data payloads
├── tests/
│   ├── smoke/            # Smoke tests
│   ├── regression/       # Regression tests
│   └── fakestore/        # FakeStore API tests
├── utils/                # Utilities (API client, logger, JSON reader)
├── .github/workflows/    # CI/CD pipelines
├── conftest.py           # Pytest fixtures
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── requirements.txt
└── README.md
```

## Features

- **API Client** with GET/POST/PUT/DELETE/PATCH methods and retry mechanism (tenacity)
- **Logging** via Loguru with rotation and retention
- **Response Validation** using Pydantic models
- **HTML Reports** auto-generated with pytest-html
- **Allure Reports** for rich test dashboards
- **Parallel Execution** with pytest-xdist
- **CI/CD** via GitHub Actions
- **Docker** containerization
- **Test Data Management** with JSON fixtures
- **FastAPI Mock Server** (`app/`) for local development and testing

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
pytest tests/fakestore/
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

Push to `main` branch triggers automatic test execution via GitHub Actions, with HTML and Allure reports uploaded as artifacts.

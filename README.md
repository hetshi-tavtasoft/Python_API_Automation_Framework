# Enterprise API Automation Framework

Enterprise-grade Python API automation framework with scalable architecture, reporting, CI/CD, Docker support, retry mechanism, and modular utilities.

## Architecture

```
enterprise-api-framework/
├── config/              # Environment configuration files
├── core/                # Core engine (API client, logger, config)
├── logs/                # Runtime logs
├── models/              # Pydantic response models
├── reports/             # HTML and Allure reports
├── testdata/            # JSON test data payloads
├── tests/
│   ├── smoke/           # Smoke tests
│   └── regression/      # Regression tests
├── utils/               # Utilities (JSON reader, etc.)
├── .github/workflows/   # CI/CD pipelines
├── Dockerfile
├── pytest.ini
├── requirements.txt
└── README.md
```

## Features

- **API Client** with GET/POST methods and retry mechanism
- **Logging** via Loguru with rotation and retention
- **Response Validation** using Pydantic models
- **HTML Reports** auto-generated with pytest-html
- **Allure Reports** for rich test dashboards
- **Parallel Execution** with pytest-xdist
- **CI/CD** via GitHub Actions
- **Docker** containerization
- **Test Data Management** with JSON fixtures

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
```

## Docker

```bash
docker build -t api-framework .
docker run api-framework
```

## CI/CD

Push to `main` branch triggers automatic test execution via GitHub Actions.

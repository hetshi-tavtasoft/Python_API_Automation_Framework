import pytest
import sys
import platform
import time
from datetime import datetime
from core.config_manager import Config
from core.api_client import APIClient
from utils.json_utils import read_json
from core.reporting import generate_report
from pytest_metadata.plugin import metadata_key

_test_results = []
_session_start = None


def pytest_configure(config):
    global _session_start
    _session_start = time.time()
    config.stash[metadata_key] = {
        "Project": "Enterprise API Automation Framework",
        "Python": sys.version.split()[0],
        "Platform": platform.platform(),
        "Base URL": Config.BASE_URL,
        "FakeStore URL": Config.FAKESTORE_BASE_URL,
        "Timeout": str(Config.TIMEOUT),
        "Retry Attempts": str(Config.RETRY_ATTEMPTS),
        "Run Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def pytest_report_header(config):
    return [
        f"Project: Enterprise API Automation Framework",
        f"Base URL: {Config.BASE_URL}",
        f"FakeStore URL: {Config.FAKESTORE_BASE_URL}",
    ]


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session):
    env = {
        "Project": "Enterprise API Automation Framework",
        "Python": sys.version.split()[0],
        "Platform": platform.platform(),
        "Base URL": Config.BASE_URL,
        "FakeStore URL": Config.FAKESTORE_BASE_URL,
        "Timeout": str(Config.TIMEOUT),
        "Retry Attempts": str(Config.RETRY_ATTEMPTS),
    }
    generate_report(
        test_results=_test_results,
        env_info=env,
        output_path="reports/dashboard.html",
        title="API Automation Test Report",
    )


def pytest_runtest_logreport(report):
    if report.when == "call":
        details = ""
        if hasattr(report, "longrepr") and report.longrepr:
            details = str(report.longrepr)
        if hasattr(report, "callspec"):
            details += f"\nParams: {report.callspec.params}"
        _test_results.append({
            "name": report.nodeid,
            "status": report.outcome,
            "duration": getattr(report, "duration", 0),
            "details": details,
        })


@pytest.fixture
def auth_token():
    return Config.API_KEY


@pytest.fixture
def auth_headers():
    return {"Authorization": f"Bearer {Config.API_KEY}"}


@pytest.fixture
def api_client():
    return APIClient


@pytest.fixture
def base_url():
    return Config.BASE_URL


@pytest.fixture
def fakestore_base_url():
    return Config.FAKESTORE_BASE_URL


@pytest.fixture
def load_json():
    return read_json

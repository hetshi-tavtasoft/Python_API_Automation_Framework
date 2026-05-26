import pytest
from utils.api_client import APIClient
from utils.logger import get_logger

@pytest.fixture
def api():
    return APIClient()

@pytest.fixture
def log():
    return get_logger("test")

@pytest.fixture(autouse=True)
def log_test_name(request):
    logger = get_logger("test")
    logger.info(f"Running test: {request.node.name}")
    yield
    logger.info(f"Finished test: {request.node.name}")

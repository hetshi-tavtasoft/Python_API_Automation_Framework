import pytest
from config.config_manager import Config
from utils.api_client import APIClient
from utils.json_reader import read_json


@pytest.fixture
def auth_token():
    """Return the API key from config."""
    return Config.API_KEY


@pytest.fixture
def auth_headers():
    """Return authorization headers using the API key."""
    return {"Authorization": f"Bearer {Config.API_KEY}"}


@pytest.fixture
def api_client():
    """Provide the APIClient class."""
    return APIClient


@pytest.fixture
def base_url():
    """Return the default base URL."""
    return Config.BASE_URL


@pytest.fixture
def fakestore_base_url():
    """Return the FakeStore base URL."""
    return Config.FAKESTORE_BASE_URL


@pytest.fixture
def load_json():
    """Return a function to load JSON test data files."""
    return read_json

import requests
import yaml
import os
from utils.logger import get_logger

log = get_logger(__name__)

def load_config():
    config_path = os.path.join("configs", "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

class APIClient:
    def __init__(self):
        config = load_config()
        self.base_url = config["base_url"]
        self.timeout = config["timeout"]
        self.session = requests.Session()
        self.session.headers.update(config.get("headers", {}))

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        log.info(f"GET {url} params={params}")
        response = self.session.get(url, params=params, timeout=self.timeout)
        log.info(f"Response {response.status_code}")
        return response

    def post(self, endpoint, data=None, json=None):
        url = f"{self.base_url}{endpoint}"
        log.info(f"POST {url}")
        response = self.session.post(url, data=data, json=json, timeout=self.timeout)
        log.info(f"Response {response.status_code}")
        return response

import time
import requests
from core.config_manager import Config
from core.logger import logger
from core.retry_handler import common_retry


class APIClient:

    @staticmethod
    def _headers(headers=None):
        defaults = {"User-Agent": "APIAutomationFramework/1.0"}
        if headers:
            defaults.update(headers)
        return defaults

    @staticmethod
    @common_retry
    def _request(method, endpoint, base_url=None, headers=None, **kwargs):
        url = f"{base_url or Config.BASE_URL}{endpoint}"

        logger.info(f"Sending {method.upper()} Request to: {url}")
        if kwargs.get("json"):
            logger.debug(f"Payload: {kwargs['json']}")
        if kwargs.get("params"):
            logger.debug(f"Params: {kwargs['params']}")

        start_time = time.time()
        try:
            response = requests.request(method, url, headers=APIClient._headers(headers), timeout=Config.TIMEOUT, **kwargs)
            elapsed = (time.time() - start_time) * 1000
            logger.info(f"Response Received | Status: {response.status_code} | Duration: {elapsed:.2f}ms")
            logger.debug(f"Response Content: {response.text[:1000]}")
            return response
        except requests.exceptions.RequestException as e:
            elapsed = (time.time() - start_time) * 1000
            logger.error(f"{method.upper()} Request failed after {elapsed:.2f}ms. Exception: {e}")
            raise

    @staticmethod
    def get(endpoint, **kwargs):
        return APIClient._request("get", endpoint, **kwargs)

    @staticmethod
    def post(endpoint, payload, **kwargs):
        return APIClient._request("post", endpoint, json=payload, **kwargs)

    @staticmethod
    def put(endpoint, payload, **kwargs):
        return APIClient._request("put", endpoint, json=payload, **kwargs)

    @staticmethod
    def patch(endpoint, payload, **kwargs):
        return APIClient._request("patch", endpoint, json=payload, **kwargs)

    @staticmethod
    def delete(endpoint, **kwargs):
        return APIClient._request("delete", endpoint, **kwargs)

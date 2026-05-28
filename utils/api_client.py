import requests
from config.config_manager import Config
from utils.logger import logger
from tenacity import retry, stop_after_attempt


class APIClient:

    @staticmethod
    @retry(stop=stop_after_attempt(3))
    def get(endpoint, base_url=None):
        url = f"{base_url or Config.BASE_URL}{endpoint}"

        logger.info(f"GET Request: {url}")

        response = requests.get(
            url,
            timeout=Config.TIMEOUT
        )

        logger.info(f"Response Status: {response.status_code}")

        return response

    @staticmethod
    @retry(stop=stop_after_attempt(3))
    def post(endpoint, payload, base_url=None):
        url = f"{base_url or Config.BASE_URL}{endpoint}"

        logger.info(f"POST Request: {url}")
        logger.info(f"Payload: {payload}")

        response = requests.post(
            url,
            json=payload,
            timeout=Config.TIMEOUT
        )

        logger.info(f"Response Status: {response.status_code}")

        return response

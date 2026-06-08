import time
import requests
from config.config_manager import Config
from utils.logger import logger
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_any,
    retry_if_exception_type,
    retry_if_result
)


def log_retry_attempt(retry_state):
    """Callback to log retry details when an attempt fails."""
    attempt = retry_state.attempt_number
    sleep_time = retry_state.next_action.sleep
    outcome = retry_state.outcome
    if outcome.failed:
        reason = str(outcome.exception())
    else:
        response = outcome.result()
        reason = f"HTTP {response.status_code}"
    
    logger.warning(
        f"Request failed. Retrying (Attempt #{attempt} in {sleep_time:.2f}s). Reason: {reason}"
    )


# Helper predicate to check for server errors that deserve retries
def is_server_error(response):
    return response is not None and response.status_code in [500, 502, 503, 504]


# Reusable retry decorator with common configuration
common_retry = retry(
    retry=retry_any(
        retry_if_exception_type(requests.exceptions.RequestException),
        retry_if_result(is_server_error)
    ),
    stop=stop_after_attempt(Config.RETRY_ATTEMPTS),
    wait=wait_exponential(multiplier=Config.RETRY_BACKOFF_FACTOR, min=1, max=10),
    before_sleep=log_retry_attempt,
    reraise=True
)


class APIClient:

    @staticmethod
    @common_retry
    def get(endpoint, base_url=None, headers=None, params=None):
        url = f"{base_url or Config.BASE_URL}{endpoint}"
        
        logger.info(f"Sending GET Request to: {url}")
        if headers:
            logger.debug(f"Headers: {headers}")
        if params:
            logger.debug(f"Params: {params}")

        start_time = time.time()
        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=Config.TIMEOUT
            )
            elapsed = (time.time() - start_time) * 1000
            
            logger.info(f"Response Received | Status: {response.status_code} | Duration: {elapsed:.2f}ms")
            logger.debug(f"Response Content: {response.text[:1000]}")
            return response
        except requests.exceptions.RequestException as e:
            elapsed = (time.time() - start_time) * 1000
            logger.error(f"GET Request failed after {elapsed:.2f}ms. Exception: {e}")
            raise

    @staticmethod
    @common_retry
    def post(endpoint, payload, base_url=None, headers=None):
        url = f"{base_url or Config.BASE_URL}{endpoint}"

        logger.info(f"Sending POST Request to: {url}")
        logger.debug(f"Payload: {payload}")
        if headers:
            logger.debug(f"Headers: {headers}")

        start_time = time.time()
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=Config.TIMEOUT
            )
            elapsed = (time.time() - start_time) * 1000

            logger.info(f"Response Received | Status: {response.status_code} | Duration: {elapsed:.2f}ms")
            logger.debug(f"Response Content: {response.text[:1000]}")
            return response
        except requests.exceptions.RequestException as e:
            elapsed = (time.time() - start_time) * 1000
            logger.error(f"POST Request failed after {elapsed:.2f}ms. Exception: {e}")
            raise

    @staticmethod
    @common_retry
    def put(endpoint, payload, base_url=None, headers=None):
        url = f"{base_url or Config.BASE_URL}{endpoint}"

        logger.info(f"Sending PUT Request to: {url}")
        logger.debug(f"Payload: {payload}")
        if headers:
            logger.debug(f"Headers: {headers}")

        start_time = time.time()
        try:
            response = requests.put(
                url,
                json=payload,
                headers=headers,
                timeout=Config.TIMEOUT
            )
            elapsed = (time.time() - start_time) * 1000

            logger.info(f"Response Received | Status: {response.status_code} | Duration: {elapsed:.2f}ms")
            logger.debug(f"Response Content: {response.text[:1000]}")
            return response
        except requests.exceptions.RequestException as e:
            elapsed = (time.time() - start_time) * 1000
            logger.error(f"PUT Request failed after {elapsed:.2f}ms. Exception: {e}")
            raise

    @staticmethod
    @common_retry
    def delete(endpoint, base_url=None, headers=None):
        url = f"{base_url or Config.BASE_URL}{endpoint}"

        logger.info(f"Sending DELETE Request to: {url}")
        if headers:
            logger.debug(f"Headers: {headers}")

        start_time = time.time()
        try:
            response = requests.delete(
                url,
                headers=headers,
                timeout=Config.TIMEOUT
            )
            elapsed = (time.time() - start_time) * 1000

            logger.info(f"Response Received | Status: {response.status_code} | Duration: {elapsed:.2f}ms")
            logger.debug(f"Response Content: {response.text[:1000]}")
            return response
        except requests.exceptions.RequestException as e:
            elapsed = (time.time() - start_time) * 1000
            logger.error(f"DELETE Request failed after {elapsed:.2f}ms. Exception: {e}")
            raise

    @staticmethod
    @common_retry
    def patch(endpoint, payload, base_url=None, headers=None):
        url = f"{base_url or Config.BASE_URL}{endpoint}"

        logger.info(f"Sending PATCH Request to: {url}")
        logger.debug(f"Payload: {payload}")
        if headers:
            logger.debug(f"Headers: {headers}")

        start_time = time.time()
        try:
            response = requests.patch(
                url,
                json=payload,
                headers=headers,
                timeout=Config.TIMEOUT
            )
            elapsed = (time.time() - start_time) * 1000

            logger.info(f"Response Received | Status: {response.status_code} | Duration: {elapsed:.2f}ms")
            logger.debug(f"Response Content: {response.text[:1000]}")
            return response
        except requests.exceptions.RequestException as e:
            elapsed = (time.time() - start_time) * 1000
            logger.error(f"PATCH Request failed after {elapsed:.2f}ms. Exception: {e}")
            raise

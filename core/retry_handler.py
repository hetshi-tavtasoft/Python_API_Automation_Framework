import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_any, retry_if_exception_type, retry_if_result
from core.config_manager import Config
from core.logger import logger


def log_retry_attempt(retry_state):
    attempt = retry_state.attempt_number
    sleep_time = retry_state.next_action.sleep
    outcome = retry_state.outcome
    if outcome.failed:
        reason = str(outcome.exception())
    else:
        response = outcome.result()
        reason = f"HTTP {response.status_code}"

    logger.warning(f"Request failed. Retrying (Attempt #{attempt} in {sleep_time:.2f}s). Reason: {reason}")


def is_server_error(response):
    return response is not None and response.status_code in {500, 502, 503, 504}


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

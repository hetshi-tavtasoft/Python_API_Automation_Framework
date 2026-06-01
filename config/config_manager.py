from dotenv import load_dotenv
import os

load_dotenv("config/qa.env")


class Config:
    BASE_URL = os.getenv("BASE_URL")
    FAKESTORE_BASE_URL = os.getenv("FAKESTORE_BASE_URL")
    API_KEY = os.getenv("API_KEY")
    TIMEOUT = int(os.getenv("TIMEOUT", "30"))
    RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "3"))
    RETRY_BACKOFF_FACTOR = int(os.getenv("RETRY_BACKOFF_FACTOR", "2"))

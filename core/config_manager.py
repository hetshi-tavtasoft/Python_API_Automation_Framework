from dotenv import load_dotenv
import os

_ENV_LOADED = False


def _load_env():
    global _ENV_LOADED
    if _ENV_LOADED:
        return
    load_dotenv("config/default.env")
    env = os.getenv("APP_ENV", "qa")
    load_dotenv(f"config/{env}.env", override=True)
    _ENV_LOADED = True


class Config:
    BASE_URL: str
    FAKESTORE_BASE_URL: str
    API_KEY: str
    TIMEOUT: int
    RETRY_ATTEMPTS: int
    RETRY_BACKOFF_FACTOR: int

    def __init_subclass__(cls, **kwargs):
        raise TypeError("Config cannot be subclassed")

    @classmethod
    def _ensure_loaded(cls):
        _load_env()
        if not hasattr(cls, "_loaded"):
            cls.BASE_URL = os.getenv("BASE_URL")
            cls.FAKESTORE_BASE_URL = os.getenv("FAKESTORE_BASE_URL")
            cls.API_KEY = os.getenv("API_KEY")
            cls.TIMEOUT = int(os.getenv("TIMEOUT", "30"))
            cls.RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "3"))
            cls.RETRY_BACKOFF_FACTOR = int(os.getenv("RETRY_BACKOFF_FACTOR", "2"))
            cls._loaded = True

    @classmethod
    def __getattr__(cls, name):
        cls._ensure_loaded()
        if name in ("BASE_URL", "FAKESTORE_BASE_URL", "API_KEY", "TIMEOUT", "RETRY_ATTEMPTS", "RETRY_BACKOFF_FACTOR"):
            return getattr(cls, name)
        raise AttributeError(f"Config has no attribute '{name}'")


Config._ensure_loaded()

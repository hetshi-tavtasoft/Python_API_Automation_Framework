from dotenv import load_dotenv
import os

load_dotenv("config/qa.env")


class Config:
    BASE_URL = os.getenv("BASE_URL")
    FAKESTORE_BASE_URL = os.getenv("FAKESTORE_BASE_URL")
    API_KEY = os.getenv("API_KEY")
    TIMEOUT = int(os.getenv("TIMEOUT"))

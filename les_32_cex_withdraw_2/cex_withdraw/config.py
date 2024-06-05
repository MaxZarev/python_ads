import os

from dotenv import load_dotenv

load_dotenv()

okx_api_key = os.getenv("okx_api_key")
okx_api_secret = os.getenv("okx_api_secret")
okx_api_secret_phrase = os.getenv("okx_api_secret_phrase")

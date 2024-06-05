import os

from dotenv import load_dotenv

load_dotenv()

okx_api_key = os.getenv("okx_api_key")
okx_api_secret = os.getenv("okx_api_secret")
okx_api_secret_phrase = os.getenv("okx_api_secret_phrase")

bybit_api_key = os.getenv("bybit_api_key")
bybit_api_secret = os.getenv("bybit_api_secret")

binance_api_key = os.getenv("binance_api_key")
binance_api_secret = os.getenv("binance_api_secret")


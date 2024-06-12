import os

from dotenv import load_dotenv

load_dotenv()


# ключи

okx_api_key = os.getenv("okx_api_key")
okx_api_secret = os.getenv("okx_api_secret")
okx_api_secret_phrase = os.getenv("okx_api_secret_phrase")

bybit_api_key = os.getenv("bybit_api_key")
bybit_api_secret = os.getenv("bybit_api_secret")

binance_api_key = os.getenv("binance_api_key")
binance_api_secret = os.getenv("binance_api_secret")

is_proxy = False

proxies = {
    "http": os.getenv("proxy"),
    "https": os.getenv("proxy")
}


# перечисления

class NameNetworks:
    class OKX:
        zksync = "zkSync Era"
        arbitrum = "Arbitrum One"

    class Binance:
        zksync = "ZKSYNC"
        arbitrum = "ARBITRUM"

    class Bybit:
        zksync = "ZKSYNC ERA"
        arbitrum = "ARBITRUM ONE"

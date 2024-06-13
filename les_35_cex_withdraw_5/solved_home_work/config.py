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
    zksync = {"OKX": "zkSync Era", "Binance": "ZKSYNCERA", "Bybit": "ZKSYNC"}
    starknet = {"OKX": "Starknet", "Binance": "STARKNET", "Bybit": "STARKNET"}
    arbitrum = {"OKX": "Arbitrum One", "Binance": "ARBITRUM", "Bybit": "ARBI"}
    optimism = {"OKX": "Optimism", "Binance": "OPTIMISM", "Bybit": "OP"}
    bsc = {"OKX": "BSC", "Binance": "BSC", "Bybit": "BSC"}
    polygon = {"OKX": "Polygon", "Binance": "MATIC", "Bybit": "MATIC"}
    avalanche = {"OKX": "Avalanche C-Chain", "Binance": "AVAXC", "Bybit": "CAVAX"}
    fantom = {"OKX": "Fantom", "Binance": "FTM", "Bybit": "FTM"}
    linea = {"OKX": "Linea", "Binance": None, "Bybit": "LINEA"}
    base = {"OKX": "Base", "Binance": "BASE", "Bybit": "BASE"}


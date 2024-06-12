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
        starknet = "Starknet"
        arbitrum = "Arbitrum One"
        optimism = "Optimism"
        bsc = "BSC"
        polygon = "Polygon"
        avalanche = "Avalanche C-Chain"
        fantom = "Fantom"
        linea = "Linea"
        base = "Base"

    class Binance:
        zksync = "ZKSYNCERA"
        starknet = "STARKNET"
        arbitrum = "ARBITRUM"
        optimism = "OPTIMISM"
        bsc = "BSC"
        polygon = "MATIC"
        avalanche = "AVAXC"
        fantom = "FTM"
        base = "BASE"

    class Bybit:
        zksync = "ZKSYNC"
        starknet = "STARKNET"
        arbitrum = "ARBI"
        optimism = "OP"
        bsc = "BSC"
        polygon = "MATIC"
        avalanche = "CAVAX"
        fantom = "FTM"
        linea = "LINEA"
        base = "BASE"

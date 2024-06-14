import random
import time
from pprint import pprint

import ccxt

from config import *
from functions import withdraw, get_wallets


def main():
    exchange = ccxt.okx({
        'apiKey': okx_api_key,
        'secret': okx_api_secret,
        'password': okx_api_secret_phrase,
    })
    wallets = get_wallets()
    random.shuffle(wallets)
    networks = [NameNetworks.arbitrum, NameNetworks.bsc, NameNetworks.optimism]
    for wallet in wallets:
        amount = random.uniform(0.001, 0.01)
        withdraw(exchange, wallet, "ETH", NameNetworks.arbitrum, amount)
        time.sleep(random.randint(300, 6000))


    # binance = ccxt.binance({
    #     'apiKey': binance_api_key,
    #     'secret': binance_api_secret
    # })
    # pprint(binance.fetch_currencies())

    # bybit = ccxt.bybit({
    #     'apiKey': bybit_api_key,
    #     'secret': bybit_api_secret,
    # })
    #
    # for exchange in [okx, binance, bybit]:
    #     print(exchange.name)
    #     pprint(exchange.fetch_balance())
    #     print()


if __name__ == '__main__':
    main()

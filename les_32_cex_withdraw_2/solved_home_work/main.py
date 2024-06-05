from pprint import pprint

import ccxt

import functions
import config
def main():


    okx = ccxt.okx({
        "apiKey": config.okx_api_key,
        "secret": config.okx_api_secret,
        "password": config.okx_api_secret_phrase
    })
    balance = functions.get_balance(okx)
    pprint(balance)

    bybit = ccxt.bybit({
        "apiKey": config.bybit_api_key,
        "secret": config.bybit_api_secret,
    })

    balance = functions.get_balance(bybit)
    pprint(balance)

    binance = ccxt.binance({
        "apiKey": config.binance_api_key,
        "secret": config.binance_api_secret,
    })

    balance = functions.get_balance(binance)
    pprint(balance)



if __name__ == "__main__":
    main()

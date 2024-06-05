from pprint import pprint

import ccxt

import functions
import config
def main():

    exchange = ccxt.okx({
        "apiKey": config.okx_api_key,
        "secret": config.okx_api_secret,
        "password": config.okx_api_secret_phrase
    })


    balance = functions.get_balance_okx(exchange)
    pprint(balance)


    # my_list = functions.get_okx_tokens()
    # for token in my_list:
    #     print(token)
    #
    # my_list = functions.get_binance_tokens()
    # for token in my_list:
    #     print(token)


if __name__ == "__main__":
    main()

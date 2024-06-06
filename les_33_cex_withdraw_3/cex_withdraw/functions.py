
import ccxt


def get_balance(exchange: ccxt.Exchange) -> dict:
    """
    Get the balance of the account
    :param exchange: подключение к бирже к конкретному аккаунту
    :return: словарь с балансами
    """
    balances = {}
    if exchange.name == "OKX":
        balances["spot"] = exchange.fetch_balance({"type": "spot"})
        balances["funding"] = exchange.fetch_balance({"type": "funding"})
    elif exchange.name == "Binance":
        balances["spot"] = exchange.fetch_balance({"type": "spot"})
        balances["funding"] = exchange.fetch_balance({"type": "funding"})
        balances["margin"] = exchange.fetch_balance({"type": "margin"})
    elif exchange.name == "Bybit":
        balances["spot"] = exchange.fetch_balance({"type": "spot"})
        balances["FUND"] = exchange.fetch_balance({"type": "FUND"})
    else:
        print("Unknown exchange")
        return {}
    return balances

def get_balance_okx(exchange: ccxt.okx) -> dict:
    """
    Get the balance of the account
    :param exchange: подключение к бирже к конкретному аккаунту
    :return:  словарь с балансами
    """
    print(exchange.name == "OKX")
    print(ccxt.binance().fetch_balance())
    print(ccxt.bybit().fetch_balance())
    balance = exchange.fetch_balance({"type": "funding"})
    return balance

def get_okx_tokens() -> list:
    my_list = list()
    markets = ccxt.okx().fetch_markets()
    for value in markets:
        my_list.append(value["symbol"])

    return my_list


def get_binance_tokens() -> list:
    my_list = list()
    markets = ccxt.binance().fetch_markets()
    for value in markets:
        my_list.append(value["symbol"])

    return my_list


if __name__ == '__main__':
    pass
    # private_api()
    # my_list = get_okx_tokens()
    # for token in my_list:
    #     print(token)
    # my_list = get_binance_tokens()
    # for token in my_list:
    #     print(token)

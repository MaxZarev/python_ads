from __future__ import annotations

import random
import time
from pprint import pprint

import ccxt



def get_wallets(path: str = "wallets.txt") -> list[str]:
    """
    Get wallets from the file with the path in the parameter
    :return: list of wallets
    """
    with open(path, "r") as file:  # Открываем файл на чтение
        wallets = file.read().split("\n")  # Читаем файл и разбиваем его по строкам
    return wallets  # Возвращаем список кошельков


def bybit_withdraw(exchange, address, token_name, network_name, amount) -> dict:
    pass


def withdraw(
        exchange: ccxt.okx | ccxt.binance | ccxt.bybit,
        address: str,
        token_name: str,
        network: dict,
        amount: float,
) -> bool:
    """
    Withdraw tokens from the exchange to the address
    :param exchange: connection to the exchange
    :param address: address of the wallet
    :param token_name: name of the token
    :param network: dictionary with the name of the network
    :param amount: amount of tokens
    :return: True if the withdrawal was successful, False otherwise
    """
    network_name = network.get(exchange.name)  # Получаем название сети в зависимости от биржи

    if exchange.name == "OKX":
        tx = okx_withdraw(exchange, address, token_name, network_name, amount)
    elif exchange.name == "Binance":
        tx = binance_withdraw(exchange, address, token_name, network_name, amount)
    elif exchange.name == "Bybit":
        tx = bybit_withdraw(exchange, address, token_name, network_name, amount)
    else:
        print("Unknown exchange")
        return False

    id_tx = tx.get("id")

    for _ in range(30):
        tx = exchange.fetch_withdrawal(id_tx)
        if tx.get("status") != "pending":
            if tx.get("status") == "ok":
                print(f"Вывод {exchange.name} {amount} {token_name} на адрес {address} в сеть {network_name} прошел успешно")
                return True
            else:
                break
        time.sleep(random.randint(30, 60))

    print(f"ОШИБКА Вывод {exchange.name} {amount} {token_name} на адрес {address} в сеть {network_name} прошел НЕ успешно, транзакция {tx}")
    return False


def get_okx_fee(exchange: ccxt.okx, token_name: str, network_name: str) -> float:
    chain = f"{token_name}-{network_name}"
    exchange.load_markets()
    currencies = exchange.currencies
    token_data = currencies.get(token_name, {})
    if token_data:
        token_networks = token_data["networks"]
        for network_data in token_networks.values():
            if chain == network_data["id"]:
                return float(network_data["fee"])
    return 0.0


def get_binance_fee(exchange: ccxt.binance, token_name: str, network_name: str) -> float:
    exchange.load_markets()
    currencies = exchange.currencies
    token_data = currencies.get(token_name, {})
    if token_data:
        token_networks = token_data['info']['networkList']
        for network_data in token_networks:
            if network_data['network'] == network_name:
                return float(network_data['withdrawFee'])
    return 0.0


def okx_withdraw(exchange: ccxt.okx, address: str, token_name: str, network_name: str, amount: float) -> dict:
    """
    Вывод любых токенов, в любых сетях с биржи okx
    :param exchange: биржа
    :param address: адрес кошелька
    :param token_name: название токена
    :param network_name: название сети
    :param amount: количество
    :return: None
    """
    fee = get_okx_fee(exchange, token_name, network_name)
    params = {
        "ccy": token_name,
        "toAddr": address,
        "amt": amount,
        "fee": fee,
        "dest": "4",
        "chain": f"{token_name}-{network_name}"
    }
    return exchange.withdraw(token_name, amount, address, params=params)


def binance_withdraw(exchange: ccxt.binance, address: str, token_name: str, network_name: str, amount: float) -> dict:
    """
    Вывод любых токенов, в любых сетях с биржи binance
    :param exchange: биржа
    :param address: адрес кошелька
    :param token_name: название токена
    :param network_name: название сети
    :param amount: количество
    :return: None
    """
    fee = get_binance_fee(exchange, token_name, network_name)
    amount -= fee
    return exchange.withdraw(token_name, amount, address, params={"network": network_name})


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
    # get_okx_fee()
    # private_api()
    # my_list = get_okx_tokens()
    # for token in my_list:
    #     print(token)
    # my_list = get_binance_tokens()
    # for token in my_list:
    #     print(token)

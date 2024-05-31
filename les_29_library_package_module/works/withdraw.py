import random

def check_balance(token_name: str, chain_name: str) -> float:
    """
    Проверяет баланс запрошенных токенов в запрошенной сети, печатает результат и возвращает его
    :param token_name: название токена
    :param chain_name: название сети
    :return: баланс запрошенного токена
    """
    print(f"Проверяем баланс {token_name} в сети {chain_name}")
    balance = random.uniform(0.1, 10.0)
    print(f"Баланс {token_name} в сети {chain_name} равен {balance}")
    return balance

def withdraw_from_binance(amount: float, token_name: str, chain_name: str) -> None:
    """
    Скрипт по выводу токенов с биржи binance
    :param amount: количество токенов
    :param token_name: название токена
    :param chain_name:  сеть вывода
    :return: None
    """
    print("upgrade")
    print(f"Вывели {amount} {token_name} в сети {chain_name} с биржи бинанс")


def withdraw_from_okx(amount: float, token_name: str, chain_name: str) -> None:
    """
       Скрипт по выводу токенов с биржи binance
       :param amount: количество токенов
       :param token_name: название токена
       :param chain_name:  сеть вывода
       :return: None
       """
    print(f"Вывели {amount} {token_name} в сети {chain_name} с биржи okx")


def withdraw_from_bybit(amount: float, token_name: str, chain_name: str) -> None:
    """
       Скрипт по выводу токенов с биржи binance
       :param amount: количество токенов
       :param token_name: название токена
       :param chain_name:  сеть вывода
       :return: None
       """
    print(f"Вывели {amount} {token_name} в сети {chain_name} с биржи bybit")


def withdraw_from_huobi(amount: float, token_name: str, chain_name: str) -> None:
    """
       Скрипт по выводу токенов с биржи binance
       :param amount: количество токенов
       :param token_name: название токена
       :param chain_name:  сеть вывода
       :return: None
       """
    print(f"Вывели {amount} {token_name} в сети {chain_name} с биржи huobi")


def withdraw_from_kucoin(amount: float, token_name: str, chain_name: str) -> None:
    """
       Скрипт по выводу токенов с биржи binance
       :param amount: количество токенов
       :param token_name: название токена
       :param chain_name:  сеть вывода
       :return: None
       """
    print(f"Вывели {amount} {token_name} в сети {chain_name} с биржи kucoin")



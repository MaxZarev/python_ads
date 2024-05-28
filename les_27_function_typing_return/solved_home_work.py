"""
Домашнее задание по function typing
"""

# задание 1

"""
Переделайте программу из 14 урока на использование функций. Найдите логические блоки кода и реализуйте по ним функции.
В итоговой программе в верхней части определены функции, в нижней реализована логика с вызовом функций.
Итоговый код с логикой программы должен сократиться и стать более понятным.
"""

import random
import time


def input_int(message: str) -> int:
    """
    Функция для ввода целого числа
    :param message: сообщение для пользователя
    :return: введенное целое число
    """
    while True:
        value = input(message)  # ввод значения
        if value.isdigit():  # если значение является целым числом
            return int(value)
        else:
            print("---- Ошибка! Введите целое число")


def generate_wallet() -> str:
    """
    Генерация случайного кошелька
    :return: кошелек
    """
    wallet = "0x"  # начало кошелька
    while len(wallet) < 42:  # пока длина кошелька меньше 42 символов
        wallet += random.choice("abcdef0123456789")  # добавляем случайный символ
    return wallet


def generate_wallets_list(wallets_amount: int) -> list:
    """
    Генерация списка кошельков
    :param wallets_amount: количество кошельков
    :return: список кошельков
    """
    wallets = []  # список кошельков
    while len(wallets) < wallets_amount:  # пока количество кошельков меньше заданного
        wallet = generate_wallet()  # генерируем кошелек
        if wallet not in wallets:  # если кошелек уникален
            wallets.append(wallet)  # добавляем кошелек в список
    return wallets


def generate_wallets_data(wallets: list) -> dict:
    my_wallets = {}  # список кошельков
    for wallet in wallets:
        eth_balance = random.uniform(0.2, 0.8)
        usdc_balance = random.randint(0, 50)

        # добавление кошелька в словарь и инициализация значений
        my_wallets[wallet] = {
            "balances": {"ETH": eth_balance, "USDC": usdc_balance},  # балансы
            "transactions": 0,  # количество транзакций
            "activities": {"swap": 0, "mint_nft": 0, "burn_nft": 0}  # количество транзакций по активностям
        }
    return my_wallets


def gas_price_generate(gas: int) -> int:
    """
    Генерация газа
    :param gas: стартовый газ
    :return: итоговый газ
    """
    gas += random.choice([-1, 1])
    if gas <= 10:  # если газ равен 10
        gas += 1  # увеличиваем газ
    elif gas >= 50:  # если газ равен 50
        gas -= 1  # уменьшаем газ
    return gas # возвращаем газ


def gas_price_checker(gas_limit: int, gas: int = 30) -> int:
    """
    Проверка и ожидание газа
    :param gas_limit: ограничение газа
    :param gas: стартовый газ
    :return: рабочий газ
    """

    while True:  # цикл ожидания газа
        gas = gas_price_generate(gas)  # генерация газа
        if gas < gas_limit:  # если газ меньше целевого значения
            print("Газ достиг нужного значения")
            break
        print(f"Газ: {gas}")  # вывод газа
        time.sleep(0.1)  # пауза
    return gas # возвращаем газ


def choice_activity(activities: dict) -> str:
    """
    Выбор активности c учетом выполненных и не выполненных активностей
    :param activities: словарь с данными по активностям
    :return: выбранную рандомную активность
    """
    if all(activities.values()) or not any(activities.values()):  # если все активности выполнены или не выполнена ни одна
        random_activity = random.choice(list(activities.keys()))  # выбор случайной активности
    else:
        zero_activities = [activity for activity in activities if not activities[activity]]  # создаем список активностей с 0 транзакций
        random_activity = random.choice(zero_activities)  # выбор случайной активности
    return random_activity # возвращаем активность


def print_wallet_data(wallet: str, data: dict) -> None:
    """
    Вывод данных по кошельку
    :param wallet: адрес кошелька
    :param data: словарь с данными по кошельку
    :return: None
    """

    print(f"Кошелек {wallet}:")
    print(f"--- Баланс ETH: {data['balances']['ETH']}")
    print(f"--- Баланс USDC: {data['balances']['USDC']}")
    print(f"--- Количество транзакций: {data['transactions']}")
    print(f"--- Количество транзакций swap: {data['activities']['swap']}")
    print(f"--- Количество транзакций mint_nft: {data['activities']['mint_nft']}")
    print(f"--- Количество транзакций burn_nft: {data['activities']['burn_nft']}")
    print()


def withdraw(balance_eth: float, wallet: str, price_activity: float) -> float:
    """
    Вывод средств с биржи
    :param balance_eth: баланс ETH
    :param wallet: кошелек
    :param price_activity: цена активности
    :return: новый баланс ETH после вывода
    """
    withdraw_amount = price_activity * 2 * random.uniform(1.1, 1.2)  # сумма вывода с биржи
    balance_eth += withdraw_amount  # добавление суммы вывода на баланс ETH
    print(f"Кошелек {wallet} вывел {withdraw_amount} ETH с биржи")
    return balance_eth


def swap(balance_eth: float, balance_usdc: float, price_activity: float) -> tuple:  # нв выводе тип данных tuple
    """
    Обмен ETH на USDC и наоборот с возвратом нового баланса
    :param balance_eth: баланс в эфире
    :param balance_usdc: баланс в usdc
    :param price_activity: цена активности
    :return: возвращаем tuple с балансами eth и usdc
    """
    eth_usdc_price = random.randint(2000, 3000)  # стоимость ETH в USDC
    if balance_usdc:  # если баланс USDC не нулевой
        balance_eth += balance_usdc / eth_usdc_price  # обмен USDC на ETH
        balance_usdc = 0  # обнуление баланса USDC
    else:
        # генерируем случайную сумму обмена между 0 и балансом ETH за вычетом стоимости транзакции
        swap_amount = random.uniform(0, balance_eth - price_activity)  # сумма обмена
        balance_eth -= swap_amount  # списываем сумму обмена
        balance_usdc += swap_amount * eth_usdc_price  # добавляем сумму обмена в USDC
    return balance_eth, balance_usdc  # возвращаем балансы


# код программы

wallets_amount = input_int(message="Введите количество кошельков: ")  # количество кошельков
min_transactions = input_int(message="Введите минимальное количество транзакций: ")  # минимальное количество транзакций

gas = random.randint(10, 50)  # стартовый газ
gas_limit = 30  # целевое значение газа

activities_prises = {
    "swap": random.randint(10, 100),
    "mint_nft": random.randint(10, 100),
    "burn_nft": random.randint(10, 100)
}  # активности и их стоимость

wallets_list = generate_wallets_list(wallets_amount=wallets_amount)  # генерация списка кошельков
my_wallets = generate_wallets_data(wallets=wallets_list)  # генерация данных по кошелькам

while True:
    wallet = random.choice(wallets_list)  # выбор случайного кошелька
    balance_eth = my_wallets[wallet]["balances"]["ETH"]  # баланс ETH
    balance_usdc = my_wallets[wallet]["balances"]["USDC"]  # баланс USDC

    gas = gas_price_checker(gas_limit=gas_limit, gas=gas)  # проверяем и ждем газ
    activities = my_wallets[wallet]["activities"]  # копируем словарь активностей и кол-ва транзакций по ним
    random_activity = choice_activity(activities)  # выбор активности

    price_activity = activities_prises[random_activity] * gas / 10000  # стоимость активности в ETH

    if price_activity > balance_eth:  # если стоимость активности больше баланса ETH
        balance_eth = withdraw(balance_eth=balance_eth, wallet=wallet, price_activity=price_activity)  # выводим средства

    if random_activity == "swap":  # если активность swap
        balance_eth, balance_usdc = swap(balance_eth=balance_eth, balance_usdc=balance_usdc, price_activity=price_activity)

    my_wallets[wallet]["balances"]["ETH"] -= price_activity  # списываем стоимость активности с баланса ETH

    print(f"Кошелек {wallet} выполнил активность {random_activity} за {price_activity} ETH")

    my_wallets[wallet]["transactions"] += 1  # увеличиваем количество транзакций
    my_wallets[wallet]["activities"][random_activity] += 1  # увеличиваем количество транзакций по активности
    my_wallets[wallet]["balances"]["ETH"] = balance_eth  # записываем баланс ETH
    my_wallets[wallet]["balances"]["USDC"] = balance_usdc  # записываем баланс ETH

    if my_wallets[wallet]["transactions"] >= min_transactions:  # если количество транзакций достигло минимального
        wallets_list.remove(wallet)  # удаляем кошелек из списка
        if not wallets_list:  # если список пуст
            break  # завершаем программу

    time.sleep(random.uniform(0.5, 1.5))  # пауза

for wallet, data in my_wallets.items():  # вывод результатов
    print_wallet_data(wallet, data)

"""
Домашнее задание по function typing
"""

# задание 1

"""
Переделайте программу из 25 урока на использование функций. Найдите логические блоки кода и реализуйте по ним функции.
В итоговой программе в верхней части определены функции, в нижней реализована логика с вызовом функций.
Итоговый код с логикой программы должен сократиться и стать более понятным.
"""

import random
import time


wallets_amount = int(input("Введите количество кошельков: "))  # количество кошельков
min_transactions = int(input("Введите минимальное количество транзакций: "))  # минимальное количество транзакций
gas = random.randint(10, 50)  # стартовый газ
gas_limit = 30  # целевое значение газа
activities_prises = {
    "swap": random.randint(10, 100),
    "mint_nft": random.randint(10, 100),
    "burn_nft": random.randint(10, 100)
}  # активности и их стоимость

my_wallets = {}  # список кошельков
for i in range(wallets_amount):
    wallet_address = "0x" + "".join([random.choice("abcdef0123456789") for _ in range(40)])  # адрес кошелька
    eth_balance = random.uniform(0.2, 0.8)  # баланс ETH
    usdc_balance = random.randint(0, 50)  # баланс USDC
    # добавление кошелька в словарь и инициализация значений
    my_wallets[wallet_address] = {
        "balances": {"ETH": eth_balance, "USDC": usdc_balance},  # балансы
        "transactions": 0,  # количество транзакций
        "activities": {"swap": 0, "mint_nft": 0, "burn_nft": 0}  # количество транзакций по активностям
    }  # добавление кошелька в словарь

wallets_list = list(my_wallets.keys())  # список кошельков
while True:
    wallet = random.choice(wallets_list)  # выбор случайного кошелька

    while True:  # цикл ожидания газа
        gas += random.choice([-1, 1])
        if gas <= 10:  # если газ равен 10
            gas += 1  # увеличиваем газ
        elif gas >= 50:  # если газ равен 50
            gas -= 1  # уменьшаем газ

        print(f"Газ: {gas}")  # вывод газа
        time.sleep(0.1)  # пауза
        if gas < gas_limit:  # если газ меньше целевого значения
            print("Газ достиг нужного значения")
            break  # завершаем цикл обновления газа

    activities = my_wallets[wallet]["activities"]  # копируем словарь активностей и кол-ва транзакций по ним
    if all(activities.values()) or not any(activities.values()):  # если все активности выполнены или не выполнена ни одна
        random_activity = random.choice(list(activities.keys()))  # выбор случайной активности
    else:
        zero_activities = [activity for activity in activities if not activities[activity]]  # создаем список активностей с 0 транзакций
        random_activity = random.choice(zero_activities)  # выбор случайной активности

    price_activity = activities_prises[random_activity] * gas / 10000  # стоимость активности в ETH

    if price_activity > my_wallets[wallet]["balances"]["ETH"]:  # если стоимость активности больше баланса ETH
        withdraw_amount = price_activity * 2 * random.uniform(1.1, 1.2)  # сумма вывода с биржи
        my_wallets[wallet]["balances"]["ETH"] += withdraw_amount  # добавление суммы вывода на баланс ETH
        print(f"Кошелек {wallet} вывел {withdraw_amount} ETH с биржи для выполнения транзакции {random_activity}")

    if random_activity == "swap":  # если активность swap
        eth_usdc_price = random.randint(2000, 3000)  # стоимость ETH в USDC
        if my_wallets[wallet]["balances"]["USDC"]:  # если баланс USDC не нулевой
            my_wallets[wallet]["balances"]["ETH"] += my_wallets[wallet]["balances"]["USDC"] / eth_usdc_price  # обмен USDC на ETH
            my_wallets[wallet]["balances"]["USDC"] = 0  # обнуление баланса USDC
        else:
            # генерируем случайную сумму обмена между 0 и балансом ETH за вычетом стоимости транзакции
            swap_amount = random.uniform(0, my_wallets[wallet]["balances"]["ETH"] - price_activity)  # сумма обмена
            my_wallets[wallet]["balances"]["ETH"] -= swap_amount  # списываем сумму обмена
            my_wallets[wallet]["balances"]["USDC"] += swap_amount * eth_usdc_price  # добавляем сумму обмена в USDC

    my_wallets[wallet]["balances"]["ETH"] -= price_activity  # списываем стоимость активности с баланса ETH

    print(f"Кошелек {wallet} выполнил активность {random_activity} за {price_activity} ETH")
    my_wallets[wallet]["transactions"] += 1  # увеличиваем количество транзакций
    my_wallets[wallet]["activities"][random_activity] += 1  # увеличиваем количество транзакций по активности

    if my_wallets[wallet]["transactions"] >= min_transactions:  # если количество транзакций достигло минимального
        wallets_list.remove(wallet)  # удаляем кошелек из списка
        if not wallets_list:  # если список пуст
            break  # завершаем программу

    time.sleep(random.uniform(0.5, 1.5))  # пауза

for wallet, data in my_wallets.items():  # вывод результатов
    print(f"Кошелек {wallet}:")
    print(f"--- Баланс ETH: {data['balances']['ETH']}")
    print(f"--- Баланс USDC: {data['balances']['USDC']}")
    print(f"--- Количество транзакций: {data['transactions']}")
    print(f"--- Количество транзакций swap: {data['activities']['swap']}")
    print(f"--- Количество транзакций mint_nft: {data['activities']['mint_nft']}")
    print(f"--- Количество транзакций burn_nft: {data['activities']['burn_nft']}")
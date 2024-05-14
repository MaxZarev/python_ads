# задание 1
"""
Напишите программу, которая будет запрашивать в терминале ввести баланс кошелька
И выводит сообщение, кем является владелец кошелька с таким балансом
0 = нищий
от 1 до 100 = нормис
от 101 до 1000 = деген
от 1001 до 10000 = кит
от 10001 и выше = Илон Маск
"""
import random

balance = int(input("Введите баланс кошелька: "))
if balance == 0:
    print("Нищий")
elif 1 <= balance <= 100:
    print("Нормис")
elif 101 <= balance <= 1000:
    print("Деген")
elif 1001 <= balance <= 10000:
    print("Кит")
else:
    print("Илон Маск")

# задание 2
"""
Напишите программу, которая генерирует цену на газ (от 10 до 100) и начальный баланс кошелька (от 2000 до 10000)
мост scroll стоит = цена газа * 75
свап внутри scroll стоит = цена газа * 40
минт домена Clusters стоит = цена газа * 100

Если на кошельке недостаточно средств на операции программа должна сначала сделать вывод нужной суммы с биржи, 
вывести сообщение о выводе и прибавить к балансу сумму вывода

Если цена на газ ниже 25, то программа запускает мост scroll, расходы должны минусоваться с баланса
Если цена на газ ниже 15, то программа после запуска моста, должна еще сминтить домен Clusters, , расходы должны минусоваться с баланса
Если цена на газ выше 25, то программа запускает свап внутри scroll, расходы должны минусоваться с баланса
Если цена на газ выше 50, то программа ничего не делает и рекомендует поработать в другой раз
В конце программа выводит сообщение о завершении работы, пишет какую работу удалось сделать и оставшийся баланс кошелька
"""
import random

gas_price = random.randint(10, 100)  # генерация цены на газ
balance = random.randint(2000, 10000)  # генерация баланса кошелька
scroll_bridge = gas_price * 75  # стоимость моста scroll
swap = gas_price * 40  # стоимость свапа внутри scroll
mint_clusters = gas_price * 100  # стоимость минта домена Clusters
min_balance = scroll_bridge + swap + mint_clusters  # минимальный баланс для операций

# флаги для отслеживания выполненных операций
withdraw_flag = False
scroll_bridge_flag = False
swap_flag = False
mint_clusters_flag = False

# вывод информации о переменных
print(f"Цена газа: {gas_price}, баланс кошелька: {balance}")
print(f"Мост scroll: {scroll_bridge}, свап: {swap}, минт домена Clusters: {mint_clusters}")
print(f"Минимальный баланс для операций: {min_balance}")

# проверка баланса на возможность выполнения операций
if balance < min_balance:
    withdraw = min_balance - balance  # сумма вывода с биржи
    print(f"Баланса не хватает на операции, необходимо вывести {withdraw}")  # вывод информации о выводе
    print(f"Вывод {withdraw} с биржи")  # вывод информации о выводе
    balance += withdraw  # увеличение баланса на сумму вывода
    print(f"Баланс увеличен на {withdraw}, новый баланс {balance}")
    withdraw_flag = True  # флаг вывода установлен

# выполнение операций в зависимости от цены на газ
if gas_price < 25:
    print("Мост scroll запущен")
    balance -= scroll_bridge  # уменьшение баланса на стоимость моста
    scroll_bridge_flag = True  # флаг моста установлен
    if gas_price < 15:  # если цена на газ ниже 15
        print("Минт домена Clusters запущен")
        balance -= mint_clusters  # уменьшение баланса на стоимость минта домена Clusters
        mint_clusters_flag = True  # флаг минта домена Clusters установлен

elif gas_price > 25 and gas_price < 50:  # если цена на газ выше 25 и ниже 50
    print("Свап внутри scroll запущен")
    balance -= swap  # уменьшение баланса на стоимость свапа
    swap_flag = True  # флаг свапа установлен
else:  # если цена на газ выше 50
    print("Рекомендуется поработать в другой раз")

print(f"Программа завершена\n Отчет:")
if withdraw_flag:  # если был сделан вывод
    print(f"--> Был сделан вывод {withdraw}")
if scroll_bridge_flag:  # если был запущен мост scroll
    print(f"--> Был запущен мост scroll на сумму {scroll_bridge}")
if mint_clusters_flag:  # если был запущен минт домена Clusters
    print(f"--> Был запущен минт домена Clusters на сумму {mint_clusters}")
if swap_flag:  # если был запущен свап внутри scroll
    print(f"--> Был запущен свап внутри scroll на сумму {swap}")
# если ничего не было сделано (все флаги False)
if not withdraw_flag and not scroll_bridge_flag and not mint_clusters_flag and not swap_flag:
    print("--> Ничего не было сделано, газ дорогой")
print(f"Оставшийся баланс кошелька: {balance}")  # вывод оставшегося баланса

# задание 3
"""
У вас есть 2 переменные с балансами кошелька в токене ETH и USDC.
Еще одна переменная описывает стоимость ETH в USDC.
Напишите программу, которая будет делать обмен из ETH в USDC если баланс USDC нулевой, при этом оставляя 5% токенов ETH на комиссии
Если баланс USDC не нулевой, то программа должна делать обмен всех токенов USDC в ETH

Во время обмена должно печататься в терминале какой токен меняется на какой и какая сумма обмена

Попробуйте сделать чтобы программа делала 5 свапов подряд по условиям выше с рандомной паузой между транзакциями.

В конце работы программа должна выводить сообщение актуальный баланс токенов ETH и USDC.
"""
import random
import time

eth_balance = random.uniform(1.0, 5.5)  # баланс ETH
usdc_balance = random.randint(1000, 10001)  # баланс USDC
eth_price = random.randint(3000, 3500)  # стоимость ETH в USDC

print(f"Баланс ETH: {eth_balance}, баланс USDC: {usdc_balance}, стоимость ETH в USDC: {eth_price}")

if usdc_balance:  # если баланс USDC не нулевой
    print(f"Обмен всех токенов {usdc_balance} USDC в {usdc_balance / eth_price} ETH")
    eth_balance += usdc_balance / eth_price  # обмен всех токенов USDC в ETH
    usdc_balance = 0  # обнуление баланса USDC
    print(f"Баланс ETH: {eth_balance}, баланс USDC: {usdc_balance}")

else:
    print(f"Обмен {eth_balance * 0.95} ETH на {eth_balance * 0.95 * eth_price} USDC")
    eth_reserve = 0.05 * eth_balance  # 5% резерва ETH
    eth_balance -= eth_reserve  # уменьшение баланса ETH на комиссию
    usdc_balance += eth_balance * eth_price  # увеличение баланса USDC на комиссию
    eth_balance = eth_reserve  # установка резерва ETH в баланс ETH
    print(f"Баланс ETH: {eth_balance}, баланс USDC: {usdc_balance}")  # вывод балансов

print("Первый обмен выполнен")

time.sleep(random.randint(1, 5))  # рандомная пауза

if usdc_balance:  # если баланс USDC не нулевой
    print(f"Обмен всех токенов {usdc_balance} USDC в {usdc_balance / eth_price} ETH")
    eth_balance += usdc_balance / eth_price  # обмен всех токенов USDC в ETH
    usdc_balance = 0  # обнуление баланса USDC
    print(f"Баланс ETH: {eth_balance}, баланс USDC: {usdc_balance}")

else:
    print(f"Обмен {eth_balance * 0.95} ETH на {eth_balance * 0.95 * eth_price} USDC")
    eth_reserve = 0.05 * eth_balance  # 5% резерва ETH
    eth_balance -= eth_reserve  # уменьшение баланса ETH на комиссию
    usdc_balance += eth_balance * eth_price  # увеличение баланса USDC на комиссию
    eth_balance = eth_reserve  # установка резерва ETH в баланс ETH
    print(f"Баланс ETH: {eth_balance}, баланс USDC: {usdc_balance}")  # вывод балансов

print("Второй обмен выполнен")

time.sleep(random.randint(1, 5))  # рандомная пауза

if usdc_balance:  # если баланс USDC не нулевой
    print(f"Обмен всех токенов {usdc_balance} USDC в {usdc_balance / eth_price} ETH")
    eth_balance += usdc_balance / eth_price  # обмен всех токенов USDC в ETH
    usdc_balance = 0  # обнуление баланса USDC
    print(f"Баланс ETH: {eth_balance}, баланс USDC: {usdc_balance}")

else:
    print(f"Обмен {eth_balance * 0.95} ETH на {eth_balance * 0.95 * eth_price} USDC")
    eth_reserve = 0.05 * eth_balance  # 5% резерва ETH
    eth_balance -= eth_reserve  # уменьшение баланса ETH на комиссию
    usdc_balance += eth_balance * eth_price  # увеличение баланса USDC на комиссию
    eth_balance = eth_reserve  # установка резерва ETH в баланс ETH
    print(f"Баланс ETH: {eth_balance}, баланс USDC: {usdc_balance}")  # вывод балансов

print("Третий обмен выполнен")

time.sleep(random.randint(1, 5))  # рандомная пауза

if usdc_balance:  # если баланс USDC не нулевой
    print(f"Обмен всех токенов {usdc_balance} USDC в {usdc_balance / eth_price} ETH")
    eth_balance += usdc_balance / eth_price  # обмен всех токенов USDC в ETH
    usdc_balance = 0  # обнуление баланса USDC
    print(f"Баланс ETH: {eth_balance}, баланс USDC: {usdc_balance}")

else:
    print(f"Обмен {eth_balance * 0.95} ETH на {eth_balance * 0.95 * eth_price} USDC")
    eth_reserve = 0.05 * eth_balance  # 5% резерва ETH
    eth_balance -= eth_reserve  # уменьшение баланса ETH на комиссию
    usdc_balance += eth_balance * eth_price  # увеличение баланса USDC на комиссию
    eth_balance = eth_reserve  # установка резерва ETH в баланс ETH
    print(f"Баланс ETH: {eth_balance}, баланс USDC: {usdc_balance}")  # вывод балансов

print("Четвертый обмен выполнен")

time.sleep(random.randint(1, 5))  # рандомная пауза

if usdc_balance:  # если баланс USDC не нулевой
    print(f"Обмен всех токенов {usdc_balance} USDC в {usdc_balance / eth_price} ETH")
    eth_balance += usdc_balance / eth_price  # обмен всех токенов USDC в ETH
    usdc_balance = 0  # обнуление баланса USDC
    print(f"Баланс ETH: {eth_balance}, баланс USDC: {usdc_balance}")

else:
    print(f"Обмен {eth_balance * 0.95} ETH на {eth_balance * 0.95 * eth_price} USDC")
    eth_reserve = 0.05 * eth_balance  # 5% резерва ETH
    eth_balance -= eth_reserve  # уменьшение баланса ETH на комиссию
    usdc_balance += eth_balance * eth_price  # увеличение баланса USDC на комиссию
    eth_balance = eth_reserve  # установка резерва ETH в баланс ETH
    print(f"Баланс ETH: {eth_balance}, баланс USDC: {usdc_balance}")  # вывод балансов

print("Пятый обмен выполнен")

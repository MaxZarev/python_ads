"""
Домашнее задание по dict
"""

# задание 1

"""
Создать функцию которая принимает 1 аргумент gas_limit, в функции в цикле должен генерироваться рандомный газ от 10 до 50, 
Если газ выше чем gas_limit, то функция должна вставать на паузу 0,1 секунду и писать уведомление в терминал,
если сгенерированный газ меньше чем gas_limit, то функция печатает "можно работать" и завершает работу.
"""
import random
import time


def wait_work_gas(gas_limit):
    """
    Функция генерирует случайное число от 10 до 50
    и печатает в терминале
    :param gas_limit: лимит газа
    :return: ничего не возвращает
    """
    while True:  # бесконечный цикл
        gas_price = random.randint(10, 50)  # генерируем случайное число
        if gas_price > gas_limit:  # проверяем больше ли газ лимита
            print(f"Газ {gas_price} больше лимита {gas_limit}")  # печатаем сообщение
            time.sleep(0.1)  # встаем на паузу
        else:  # если газ меньше лимита
            print("Можно работать")  # печатаем сообщение
            break  # выходим из цикла и заканчиваем работу функции


# задание 2

"""
Создать функцию генератор паролей, которая принимает 4 аргумента: длину пароля, а так же 3 аргумента bool (true/false):
1. использовать ли латинские буквы
2. использовать ли цифры
3. использовать ли спец символы
Функция должна генерировать пароль с использованием выбранных символов и печатать его в терминале.
"""

import random
import string

def password_generator(len_password, is_lat_symbol, is_numbers, is_spec_symbol):
    """
    Функция генерирует пароль по заданным параметрам и печатает в терминале.
    :param len_password: длина пароля, минимум 3 символа
    :param is_lat_symbol: использовать ли латинские буквы
    :param is_numbers: использовать ли цифры
    :param is_spec_symbol: использовать ли спец символы
    :return: None
    """

    if not any([is_lat_symbol, is_numbers, is_spec_symbol]):
        print("Необходимо выбрать хотя бы один тип символов")
        return

    if len_password < 3:
        print("Длина пароля должна быть больше 2")
        return


    password = ""  # создаем переменную для пароля
    alphabet = string.ascii_letters  # латинские буквы (включая заглавные)
    number = string.digits  # цифры
    spec_symbol = "!@#$%^&*()_+-="  # спец символы

    active_symbols_list = []

    # Добавляем минимум по одному символу каждого типа если нужно и собираем выбранные символы в список
    if is_lat_symbol:
        password += random.choice(alphabet)
        active_symbols_list.append(alphabet)
    if is_numbers:
        password += random.choice(number)
        active_symbols_list.append(number)
    if is_spec_symbol:
        password += random.choice(spec_symbol)
        active_symbols_list.append(spec_symbol)

    # Добавляем остальные символы
    for _ in range(len_password - len(password)): # пока длина пароля не равна нужной
        random_symbols = random.choice(active_symbols_list) # выбираем случайный список символов
        password += random.choice(random_symbols) # добавляем случайный символ из выбранного списка

    password = ''.join(random.sample(password, len(password))) # перемешиваем пароль
    print(password)  # печатаем пароль

# задание 3

"""
Создать функцию генератор кошельков, которая принимает 1 аргумент, количество кошельков и генерирует список из нужного количества кошельков
в формате "0x" + 40 случайных символов из набора "abcdef0123456789" (16-ричная система исчисления).
Итоговый список должен быть сохранен в через глобальную переменную wallets снаружи функции, чтобы полученный список можно было использовать вне функции.
"""
wallets = []
def generate_wallet_list(wallet_amount):
    """
    Функция генерирует список кошельков в формате "0x" + 40 случайных символов из набора "abcdef0123456789" и сохраняет в глобальную переменную wallets

    :param wallet_amount: количество кошельков которое нужно сгенерировать
    :return: None
    """
    global wallets  # обращаемся к глобальной переменной
    while len(wallets) < wallet_amount:  # пока в списке не будет нужное количество кошельков
        wallet = "0x"  # начало кошелька

        # добавляем случайные символы в кошелек пока он не станет длиной 42 символа
        while len(wallet) < 42:
            wallet += random.choice("abcdef0123456789")  # добавляем случайный символ

        # проверяем что кошелек уникален
        if wallet not in wallets:
            wallets.append(wallet)  # добавляем кошелек в список


# задание 4

"""
Создать функцию вывода с биржи, на вход должна получать адрес кошелька и минимальный баланс, внутри должен проходить псевдо запрос баланса (генерируем рандомно), 
если баланс ниже минимальной суммы делать вывод на кошелек рандомной суммы и напечатать сообщение об этом.
"""

def withdraw_from_exchange(wallet, min_balance):
    """
    Функция вывода с биржи, на вход должна получать адрес кошелька и минимальный баланс, внутри должен проходить псевдо запрос баланса (генерируем рандомно),
    :param wallet: адрес кошелька
    :param min_balance: минимальный баланс
    :return: None
    """
    balance = random.randint(0, 2000)  # генерируем случайный баланс
    print(f"Баланс кошелька {wallet}: {balance}")  # печатаем баланс
    if balance < min_balance:  # проверяем что баланс ниже минимальной суммы
        amount = random.randint(100, 1000)  # генерируем случайную сумму
        print(f"Вывод на кошелек {wallet} суммой {amount}")  # печатаем сообщение о выводе



# задание 6

"""
Используя созданные функции создайте программу, которая:
создает список кошельков
Потом в цикле перебирает список кошельков и делает следующее:
Печатает название кошелька.
Генерирует новый пароль при помощи функции и печатает его в терминале.
Ждет когда газ будет меньше 30 и печатает уведомление в терминале.
Проверяет баланс кошелька, если баланс меньше 1000 делает вывод на кошелек рандомной суммы.

Функции должны быть определены в верхней части программы, логика программы и вызов функций в нижней части.
"""

wallets = []
generate_wallet_list(10)  # генерируем список кошельков
for wallet in wallets:
    print(f"Кошелек: {wallet}")  # печатаем название кошелька
    password_generator(10, True, True, True)  # генерируем пароль
    wait_work_gas(30)  # ждем когда газ будет меньше 30
    withdraw_from_exchange(wallet, 1000)  # проверяем баланс и делаем вывод если надо
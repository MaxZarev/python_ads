"""
Домашнее задание по list
"""

# задание 1

"""
Вы вводите в терминале любой текст через пробел, программа должна напечатать список в котором все слова в обратном порядке, 
отдельное слово в отдельном элементе списка.
"""
text = input("Введите текст через пробел: ")
text_list = text.split()
print(text_list[::-1])

# задание 2
"""
Возьмите предыдущее задание 3 из урока по while где нужно было раздать дроп рандомным кошелькам и доработайте программу таким образом чтобы кошельки, которые получают
дроп собирались в список и в конце печатался список кошельков получивших дроп, а не строчка.
"""

import time
import random

gas_price = 50
while True:
    wallets_amount = input("Введите количество кошельков: ")
    if wallets_amount.isdigit():
        wallets_amount = int(wallets_amount)
        break
    else:
        print("Ошибка, введите число")

while True:
    drops_amount = input("Введите количество дропов: ")
    if drops_amount.isdigit():
        drops_amount = int(drops_amount)
        break
    else:
        print("Ошибка, введите число")

wallets_with_drop = []
wallet_number = 0

while wallet_number < wallets_amount:

    wallet_number += 1

    if random.randint(0, 1) and drops_amount > 0:
        print(f"Кошелек номер: {wallet_number} получил дроп")
        wallets_with_drop.append(wallet_number)
        while gas_price > 50:
            print(f"Цена на газ {gas_price} выше порога 20")
            time.sleep(1)
            gas_price = random.randint(15, 50)
        print(f"Дроп клеймится, газ {gas_price}")
        drops_amount -= 1
        gas_price = 50
    else:
        print(f"Кошелек номер: {wallet_number} не получил дроп")

    if drops_amount != 0 and wallet_number == wallets_amount:
        wallet_number = 0


print(f"Кошельки с дропом: {wallets_with_drop}")


# задание 3

"""
Создайте при помощи цикла while список в котором будут перечислены четные числа от 1 до 100 включительно. (пример: [2, 4, 6, 8, 10, ...])
В во втором цикле while замените все числа на эти же числа в квадрате.
Доработайте программу так чтобы можно было ввести диапазон чисел для создания списка.
"""
min_num = int(input("Введите минимальное число: "))
max_num = int(input("Введите минимальное число: "))

numbers_list = []
counter = min_num - 1
while counter < max_num:
    counter += 1
    if counter % 2 == 0:
        numbers_list.append(counter)

print(numbers_list)

counter = 0
while counter < len(numbers_list):
    numbers_list[counter] = numbers_list[counter] ** 2
    counter += 1

print(numbers_list)

# задание 4
"""
Создайте генератор списков паролей, который будет запрашивать диапазон длины пароля (от скольки до скольки символов), какие символы должны входить в пароль, 
а так же количество паролей.
На выходе должен получаться список с необходимым количеством паролей и в соответствии с запросом пользователя.
"""
length_min = int(input("Введите минимальную длину пароля: "))
length_max = int(input("Введите максимальную длину пароля: "))
is_symbols = input("Включать ли символы? (да/нет): ")
is_digits = input("Включать ли цифры? (да/нет): ")
is_uppercase = input("Включать ли заглавные буквы? (да/нет): ")
is_lowercase = input("Включать ли строчные буквы? (да/нет): ")

symbols = "!@#$%^&*()_+{}[]"
digits = "0123456789"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowercase = uppercase.lower()

passwords_amount = int(input("Введите количество паролей: "))

passwords = []

while passwords_amount > 0:
    password = ""
    password_length = random.randint(length_min, length_max)

    # добавляем по одному символу каждого типа
    if is_symbols == "да" and len(password) < password_length:
        password += random.choice(symbols)
    if is_digits == "да" and len(password) < password_length:
        password += random.choice(digits)
    if is_uppercase == "да" and len(password) < password_length:
        password += random.choice(uppercase)
    if is_lowercase == "да" and len(password) < password_length:
        password += random.choice(lowercase)

    while len(password) < password_length:

        # выбираем рандомный тип символа
        # 0 - symbols, 1 - digits, 2 - uppercase, 3 - lowercase
        random_symbol_type = random.randint(0, 3)

        if random_symbol_type == 0:
            if is_symbols == "да":
                password += random.choice(symbols)
        elif random_symbol_type == 1:
            if is_digits == "да":
                password += random.choice(digits)
        elif random_symbol_type == 2:
            if is_uppercase == "да":
                password += random.choice(uppercase)
        elif random_symbol_type == 3:
            if is_lowercase == "да":
                password += random.choice(lowercase)

    passwords.append(password)
    passwords_amount -= 1

print(passwords)

# задание 5

"""
Создайте программу которая генерирует рандомный газ, при этом газ с вероятностью 50% должен увеличиваться или уменьшаться на 1 единицу раз в секунду.
Программа должна замерять газ за минуту и выводить его в виде списка, а так же печатать среднее значение газа за последнюю минуту.
"""

import time
import random

gas = random.randint(1, 100)
gas_list = []
counter = 0
while counter < 60:
    counter += 1
    gas_list.append(gas)
    if random.randint(0, 1):
        gas += 1
    else:
        gas -= 1
    time.sleep(1)

print(gas_list)
print(sum(gas_list) / len(gas_list))

# задание 6
"""
Создайте список из 10 разных активностей. Программа должна спрашивать сколько транзакций нужно выполнить.
Создайте программу которая будет рандомно выбирать одну из активностей и выполнять ее (печатать в консоль), после рандомной паузы повторяет 
пока не сделает запрошенное количество транзакций.

HARD LEVEL: 
доработай программу так чтобы она печатала сколько раз была выполнена каждая активность.
"""
# вариант 1

import time
import random

activities = ["bridge", "swap", "mint", "transfer", "like", "repost", "activity7", "activity8", "activity9", "activity10"]

transactions_amount = int(input("Введите количество транзакций: "))
counter = 0
while counter < transactions_amount:
    counter += 1
    activity = random.choice(activities)
    print(f"делаем {activity}")
    time.sleep(random.randint(1, 3))

# hard level
import time
import random
activities = ["bridge", "swap", "mint", "transfer", "like", "repost", "activity7", "activity8", "activity9", "activity10"]
activities_counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

transactions_amount = int(input("Введите количество транзакций: "))
counter = 0
while counter < transactions_amount:
    counter += 1
    random_index = random.randint(0, 9)
    activity = activities[random_index]
    activities_counter[random_index] += 1
    print(f"делаем {activity}")
    time.sleep(random.randint(1, 3))

counter = 0
while counter < len(activities):
    print(f"{activities[counter]} - {activities_counter[counter]}")
    counter += 1
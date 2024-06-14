# задание 1
"""
Напишите программу, которая генерирует случайное целое число между двумя введенными числами
и выводит сообщение о выводе токенов с биржи на кошелек
с указанной суммой
"""

import random

# вариант 1
random_number = random.randint(1, 100)  # генерируем случайное число
print(f"Выводим с биржи на кошелек {random_number} токенов")  # выводим сообщение

# вариант 2
print(f"Выводим с биржи на кошелек {random.randint(1, 100)} токенов")  # выводим сообщение

# вариант 3
min_amount = int(input("Введите минимальное число: "))  # запрашиваем у пользователя минимальное число
max_amount = int(input("Введите максимальное число: "))  # запрашиваем у пользователя минимальное число
random_amount = random.randint(min_amount, max_amount)  # генерируем случайное число
print(f"Выводим с биржи на кошелек {random_amount} токенов")  # выводим сообщение

# задание 2
"""
Доработайте код так, чтобы при сложении переменной number и числа 10 получалось 25, при этом
использовать математические операции с числами запрещено, только встроенные функции
"""

number = -15
number = abs(number)  # преобразуем число в положительное при помощи функции abs()
print(number + 10)  # должно вывести 25

# задание 3
"""
Написать программу которая запрашивает число у пользователя через функцию input()
и выводит сообщение о том, является ли число четным или нечетным - True или False
"""
number = int(input("Введите число: "))  # запрашиваем число у пользователя и преобразуем его в целое число
print(number % 2 == 0)  # делим введеное число на 2 и сравниваем остаток с 0

# задание 4
"""
Создайте 3 переменные с характеристиками кошелька: баланс, количество транзакций, объем транзакций.
Создайте 4 переменные с минимальными критерием дропа: объем, количество транзакций, средняя сумма транзакции
и баланс и подставьте желаемые значения.
Обратите внимание что значение средней суммы транзакции у кошелька нужно высчитывать
на основе других переменных кошелька.
Чтобы быть Eligible нужно чтобы все значения были больше минимальных критериев.
Напишите программу, которая проверяет Eligible и выводит True или False, 
"""
# вариант 1

balance = 1000  # баланс кошелька
number_of_transactions = 5  # количество транзакций
volume_of_transactions = 100  # объем транзакций
average_transaction_amount = volume_of_transactions / number_of_transactions  # средняя сумма транзакции кошелька

min_volume = 50  # минимальный объем транзакций
min_number_of_transactions = 3  # минимальное количество транзакций
min_average_transaction_amount = 75  # минимальная средняя сумма транзакции
min_balance = 500  # минимальный баланс

print(
    volume_of_transactions > min_volume and number_of_transactions > min_number_of_transactions and average_transaction_amount > min_average_transaction_amount and balance > min_balance)

# вариант 2

balance = int(input("введите баланс кошелька "))  # баланс кошелька
number_of_transactions = int(input("введите количество транзакций кошелька "))  # количество транзакций
volume_of_transactions = int(input("введите объем транзакций  кошелька "))  # объем транзакций
average_transaction_amount = volume_of_transactions / number_of_transactions  # средняя сумма транзакции кошелька

min_volume = 50  # минимальный объем транзакций
min_number_of_transactions = 3  # минимальное количество транзакций
min_average_transaction_amount = 75  # минимальная средняя сумма транзакции
min_balance = 500  # минимальный баланс

# проверяем условия, через логический оператор and, результат True или False кладем в переменную
eligible = volume_of_transactions > min_volume and number_of_transactions > min_number_of_transactions and average_transaction_amount > min_average_transaction_amount and balance > min_balance

print("Eligible:", eligible)  # выводим результат проверки

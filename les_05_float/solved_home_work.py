
# задание 1
"""
Найти информацию об форматировании float чисел в f-строчках и попробовать написать код,
который будет округлять число для вывода в терминале без функции round()
f"Ваше число: {number}"
"""

balance = 10.55051651
print(f"Ваше число: {balance:.4f}")  # выводим число с округлением до 4 символов после точки

# задание 2
"""
Написать программу которая имитирует вывод случайной суммы токенов ETH с биржи,
код должен генерировать случайную сумму вывода между 0.001 и 0.09 с округлением до 4 символов после точки.
И выводить в терминале сообщение "Ваша сумма вывода: {случайное число} ETH"
"""
import random

amount_eth = random.uniform(0.001, 0.09)  # генерируем случайное число с плавающей точкой
print(f"Ваша сумма вывода: {amount_eth:.4f} ETH")  # выводим сообщение с округлением до 4 символов после точки
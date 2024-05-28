# # функции и методы
import random

#
# tokens = ["USDT", "ETH", "BNB"]
#
# len_list = len(tokens)
#
# len_list = 0
# for token in tokens:
#     len_list += 1
# print(len_list)
#
#
# tokens.append("BTC")
print("Перед функцией")


# def print_random_gas():
#     """
#     Функция генерирует случайное число от 10 до 50
#     и печатает в терминале
#     :return: None
#     """
#     global gas_price
#     gas_price = random.randint(10, 50)
#     print(gas_price)

def print_random_gas(min_gas, max_gas):
    """
    Функция генерирует случайное число от 10 до 50
    и печатает в терминале
    :param min_gas: минимальное значение
    :param max_gas: максимальное значение
    :return: None
    """
    gas_price = random.randint(min_gas, max_gas)
    print(gas_price)


gas_price = 0

print("Запускаем в работу")
print_random_gas(min_gas=10, max_gas=50)
print("Работаем")
print_random_gas(min_gas="50", max_gas="70")

print("Завершаем работу")

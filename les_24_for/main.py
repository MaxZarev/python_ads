# счетчик
# counter = 0
# while counter < 5:
#     print('Counter:', counter)
#     counter += 1
import random

# counter = range(0, 10, 1)  # 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
# print(type(counter))
# my_list = list(counter)
# print(my_list)
# my_list = list(range(50, 100))
# print(my_list)

# счетчик
# counter = 0
# while counter < 100:
#     print('Counter:', counter)
#     counter += 1

# for i in range(0, 1000, 5): # 0, 5, 10, 15, 20, 25, 30, 35, 40, 45
#     print('Counter:', i)


# my_list = ["one", "two", "three", "four", "five"]
# list_len = len(my_list)
# for i in range(list_len):
#     print(my_list[i])

# for i in my_list:
#     print(i)

# wallets = ["0x....af", "0x....35", "0x....4а"]
# transactions = [5, 7, 3]
#
# for i, wallet in enumerate(wallets):
#     print(f"Wallet: {wallet}, number: {i+1}")
#     print(f"Transaction: {transactions[i]}")

# for transaction, wallet in zip(transactions, wallets):
#     print(f"Wallet: {wallet}, transaction: {transaction}")
#
# for transaction, wallet in zip(transactions, wallets):
#     print(f"Wallet: {wallet}, transaction: {transaction}")
#
# for i in range(100):
#     print(f"Внешний цикл: {i}")
#     for j in range(10):
#         print(f"Внутренний цикл: {j*i}")

# wallets = ["0x....af", "0x....35", "0x....4а"]
# tokens = ["USDC", "TROB", "ETH"]
#
# for wallet in wallets:
#     for i in range(100):
#         for token in tokens:
#             amount = random.randint(1, 100)
#             if amount < 50:
#                 continue
#             elif amount == 1:
#                 break
#             print(f"Wallet: {wallet}, вывод token: {token} {amount}")
#
# for _ in range(500):
#     print("Повторная операция")

# # создание списка циклом
# my_list = []
# counter = 0
# while counter < 5:
#     my_list.append(counter)
#     counter += 1
# print(my_list)
#
# # перебор списка циклом
# index = 0
# while index < len(my_list):
#     print(my_list[index])
#     index += 1

# my_list = []
# for i in range(10):
#     my_list.append(i)
#
# print(my_list)

# my_list = [i for i in range(10)]
# print(my_list)

tokens = ["USDC", "TROB", "ETH"]
new_tokens = [token.lower() for token in tokens if token != "ETH"]
print(new_tokens)

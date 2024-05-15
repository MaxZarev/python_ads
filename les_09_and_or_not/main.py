# если условие == True:
#     то, выполняется этот блок
# либо если условие == что-нибудь:
#     то, выполняется этот блок
# иначе (если ни одно из условий не выполнилось):
#     то, выполняется этот блок

# # 0 - False, любое другое число - True
# balance = 1
# print(1 < 2)
#
# if balance:
#     print('Баланс положительный')
#     print("Запускаем работу")
# else:
#     print('Баланс нулевой')
#     print(f"делаем вывод с биржи")


# # 0 - False, любое другое число - True
# print(1 < 2)
# если ты видишь слово not, инвертируй булево значение в противоположное
# True <-> False
# False <-> True

# balance = 1
#
# if not balance:
#     print('Баланс нулевой')
#     print(f"делаем вывод с биржи")
#
# print('Баланс положительный')
# print("Запускаем работу")


# gas_price = 21
# tx_counter_in_wallet = 20
#
# GAS_LIMIT = 20
# tx_counter_target = 30

# print(1 + 1 * 2 / 3 + (2 - 1))
# if True and True:
#     print('Запускаем в работу')
# print(0 * 0)
# print(0 * 1)
# print(1 * 0)
# print(1 * 1)
# print(False and False)
# print(True and False)
# print(False and True)
# print(True and True and True and True and True)
#
# if gas_price < GAS_LIMIT and tx_counter_in_wallet < tx_counter_target:
#     print('Запускаем в работу')

# print(False or False)
# print(True or False)
# print(False or True)
# print(True or True)
# print(0 + 0)
# print(0 + 1)
# print(1 + 0)
# print(1 + 1)
#
# balance_usdt = 1
# balance_eth = 0
#
# gas_price = 19
# GAS_LIMIT = 20
#
#
# if (balance_usdt > 0 or balance_eth > 0) and gas_price < GAS_LIMIT:
#     print('Запускаем в работу')


# balance_usdt = 1
# balance_eth = 0
# gas_price = 19
# GAS_LIMIT = 20
#
# if (balance_usdt > 0 or balance_eth > 0) and gas_price < GAS_LIMIT:
#     if balance_usdt > 0:
#         print('Меняем USDT на ETH')
#     else:
#         print('Меняем ETH на USDT')
#
#     print('Запускаем в работу')
#
#     if balance_usdt > 0:
#         print('Меняем USDT на ETH')
#         if balance_usdt > 0:
#             print('Меняем USDT на ETH')
#         else:
#             print('Меняем ETH на USDT')
#     else:
#         print('Меняем ETH на USDT')
#         if balance_usdt > 0:
#             print('Меняем USDT на ETH')
#         else:
#             print('Меняем ETH на USDT')

time = 13 # 24 часовой формат

if time < 12:
    type_of_day = "утро"
else:
    type_of_day = "день"

print(f"Сейчас {type_of_day}")

type_of_day = "утро" if time < 12 and True else "день"


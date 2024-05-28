# тип данных словарь - dict
# dict()
#
# wallets = ["0x....af", "0x....35", "0x....4а"]
#
# tokens = ["USDC", "ETH", "BNB", "BTC"]
# balances = [1000, 1.5, 20, 0.0054]
# tokens_and_balances = [
#     [["USDC", 1000], ["ETH", 1.5], ["BNB", 20], ["BTC", 0.0054]],
#     [["USDC", 1000], ["ETH", 1.5], ["BNB", 20], ["BTC", 0.0054]],
#     [["USDC", 1000], ["ETH", 1.5], ["BNB", 20], ["BTC", 0.0054]]]
#
# for i in range(len(tokens)):
#     print(f"Токен: {tokens[i]}, баланс: {balances[i]}")
#
# # словарь - dict - это структура данных, которая хранит данные в формате ключ: значение
#
#
# """
# название поля - значение пол
# название - значение
# имя поля - значение поля
# имя - значение
# ключ - значение
# ключевое слово - значение
#
# название токена - баланс токена
# USDT - 10
# ETH - 1.5
# BNB - 20
#


# my_dict = dict()
# my_dict2 = {}
# print(type(my_dict))
# print(my_dict)

# balances = {"USDT": 10, "ETH": 1.5, "BNB": 20}
# my_data = {"name": "Max", "age": 31}
# my_wallet = {"address": "0x....af", "balance": 1000, "txs": 50}
# dict
# balances = {"USDT": 10, "ETH": 1.5, "BNB": 20}
# usdt_balance = balances["UST"]
# print(usdt_balance)

# balances = {"USDT": 10, "ETH": 1.5, "BNB": 20}  # None
# token_balance = balances.get("UST", -1)
# print(token_balance)
# print("UST" in balances)
# if "USDT" in balances:
#     print(balances["USDT"])

# balances = {"USDT": 10, "ETH": 1.5, "BNB": 20}
# print(balances)
# balances["USDC"] = 500
# print(balances)
# balances["USDT"] += 5
# print(balances)

# balances = {"USDT": 10, "ETH": 10, "BNB": 10}
# token_name = "USDC"
# balances[token_name] = 1000
# print(balances)
# balances.get(token_name, 0)
# print(balances[token_name])

# balances = {"USDT": 10, "ETH": 10, "BNB": 10}
# print(id(balances))

# pop()
# balances.pop("USDT")
# # print(balance)
# print(balances)

# popitem()
# last_balance = balances.popitem()
# print(type(last_balance))
# print(last_balance)
# print(balances)
#
# del

# del balances["USDT"]
# print(balances)
#
#
# # clear()
# balances.clear()
# print(balances)
#
# print(id(balances))
#
# copy_balances = balances.copy()
# print(id(copy_balances))

balances = {"USDT": 10, "ETH": 20, "BNB": 30}

# for key in balances:
#     print(key)
#     print(balances[key])


# for value in balances.values():
#     print(value)

# for token_name, balance in balances.items():
#     print(f"Токен: {token_name}, баланс: {balance}")

my_acc = {
    "id_ads": "jndsfjsn",
    "address": "0x....af",
    "twitter": "MaxZarev",
    "discord": "MaxZarev#1234"
}
# print(my_acc["address"])

my_accs = {
    "acc_1": {
        "id_ads": "jndsfjsn",
        "address": "0x....af",
        "twitter": "MaxZarev",
        "discord": "MaxZarev#1234"
    },
    "acc_2": {
        "id_ads": "sdfsdffsd",
        "address": "0x....5f",
        "twitter": "Vasya",
        "discord": "Vasya#1234"
    },
}
print(my_accs["acc_2"]["address"])

gas_price = 5
eth_price = 3100
print(f"Стоимость газа {gas_price} gwei")
transaction_price = 21000 * gas_price / 10 ** 9
print(f"Стоимость транзакции 21000 gas * {gas_price} gwei = {transaction_price} ETH или {transaction_price * eth_price} $")
print("Для получения дропа нужно сделать 100 транзакций")
print(f"Расход для получения дропа составит {gas_price} gwei = {transaction_price * 100} ETH")
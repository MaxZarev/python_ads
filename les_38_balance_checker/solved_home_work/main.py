from web3 import Web3
from config import *


def get_native_balance(w3: Web3, address: str) -> float:
    address = Web3.to_checksum_address(address) # приводим адрес к нужному формату
    wei = w3.eth.get_balance(address) # получаем баланс в wei
    return wei / 10 ** 18 # возвращаем баланс в нужном формате


def get_wallets() -> list:
    with open('wallets.txt') as f: # читаем файл с кошельками
        return f.read().splitlines() # возвращаем список кошельков


def record_result(wallets: list, network_name: str, balances: list) -> None:
    with open(f'{network_name}.txt', 'w') as f: # записываем результат в файл
        for address, balance in zip(wallets, balances): # итерируемся по списку кошельков и балансов
            f.write(f'{address} {balance} {NETWORKS[network_name]["native"]}\n') # записываем информацию о кошельке

def user_selects_network()->str:
    network_names = list(NETWORKS.keys())  # получаем список названий сетей

    for num, network_name in enumerate(network_names, start=1):  # печатаем список сетей и номера для пользователя
        print(num, network_name)

    # пользователь выбирает сеть, результат уменьшаем, чтобы использовать как индекс списка
    choice = int(input('Выберите сеть (введите номер):\n')) - 1
    return network_names[choice]  # получаем название сети


def main():
    network_name = user_selects_network()  # получаем название сети
    network = NETWORKS[network_name]  # получаем словарь сети
    wallets = get_wallets()  # получаем список кошельков
    w3 = Web3(Web3.HTTPProvider(network['rpc']))  # создаем объект Web3

    balances = []  # список балансов кошельков
    total_balance = 0  # суммарный баланс

    for num, address in enumerate(wallets, start=1):  # итерируемся по списку кошельков
        balance = get_native_balance(w3, address)  # получаем баланс кошелька
        balances.append(balance)  # добавляем баланс в список
        total_balance += balance  # увеличиваем суммарный баланс
        print(f'{num}. {address} {balance} {network["native"]}')  # печатаем информацию о кошельке

    print(f'Кошельков проверенно: {len(wallets)}')
    print(f'Суммарный баланс: {total_balance} {network["native"]}')

    record_result(wallets, network_name, balances) # записываем результат в файл


if __name__ == '__main__':
    main()

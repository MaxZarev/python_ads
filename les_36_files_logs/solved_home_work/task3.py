import requests

from task2 import list_to_lower, write_list_to_file
from task1 import get_wallets


def main():
    url = 'https://raw.githubusercontent.com/ZKsync-Association/zknation-data/main/eligibility_list.csv'
    response = requests.get(url)  # запрашиваем данные по url
    data = response.text  # получаем текст из ответа

    with open('data/eligibility_list.csv', 'w') as f:
        f.write(data)  # записываем данные в файл

    data_wallets_drop = get_wallets('data/eligibility_list.csv')  # получаем список кошельков с суммой дропа из файла eligibility_list.csv
    wallets = get_wallets()  # получаем список кошельков из файла wallets.txt
    wallets = list_to_lower(wallets)  # приводим все кошельки к нижнему регистру
    wallets_with_drop_dict = {}  # словарь кошельков с суммой дропа

    # преобразуем список кошельков с суммой дропа в словарь
    for wallet_with_amount in data_wallets_drop[1:]:  # пропускаем первую строку с заголовками
        if wallet_with_amount:  # если строка не пустая
            wallet, amount = wallet_with_amount.split(',')  # разделяем кошелек и сумму дропа
            wallets_with_drop_dict[wallet.lower()] = int(amount)  # добавляем кошелек и сумму дропа в словарь

    wallets_with_drop = []  # список кошельков, которые получили дроп
    wallets_status = []  # список всех кошельков с проставленным статусом и суммой
    total_amount = 0  # общая сумма дропа

    # проверяем наличие кошелька в списке кошельков с суммой дропа
    for wallet in wallets:
        amount = wallets_with_drop_dict.get(wallet, 0)  # получаем сумму дропа по кошельку из словаря или 0
        if amount:  # если сумма дропа больше 0
            total_amount += amount  # считаем общую сумму дропа
            status = 'ELIGIBLE'  # статус кошелька
            wallets_with_drop.append(f"{wallet}-{status}-{amount}")  # добавляем кошелек в список кошельков, которые получили дроп
        else:
            status = 'NOT ELIGIBLE'

        wallets_status.append(f"{wallet}-{status}-{amount}") # добавляем кошелек в список всех кошельков с проставленным статусом и суммой
        print(f"{wallet}-{status}-{amount}")

    print(f"Количество кошельков, которые получили дроп: {len(wallets_with_drop)}")
    print(f"Сумма дропа: {total_amount}")

    # записываем список кошельков, которые получили дроп, в файл wallets_with_drop.txt
    write_list_to_file("data/wallets_with_drop.txt", wallets_with_drop)
    # записываем список всех кошельков с проставленным статусом и суммой, в файл wallets_status.txt
    write_list_to_file("data/wallets_status.txt", wallets_status)


if __name__ == '__main__':
    main()

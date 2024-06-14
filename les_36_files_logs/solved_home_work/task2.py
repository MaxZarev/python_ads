from task1 import get_wallets

def list_to_lower(data: list) -> list:  # функция для приведения всех элементов списка к нижнему регистру
    """
    The function converts all elements of the list to lowercase.
    :param data: list with str elements with random case
    :return: list with str elements in lowercase
    """
    return [item.lower() for item in data]

def write_list_to_file(file_path: str, data: list) -> None:  # функция для записи списка в файл
    """
    The function writes a list to a file.
    :param file_path: path to result file
    :param data: list of data
    :return: None
    """
    with open(file_path, "w") as file:
        for item in data:
            file.write(item + "\n")


def main():
    wallets = get_wallets()  # получаем список кошельков из файла wallets.txt
    eligibility_list = get_wallets("data/zksync_eligibility_list.txt")  # получаем список кошельков из файла zksync_eligibility_list.txt

    wallets = list_to_lower(wallets)  # приводим все кошельки к нижнему регистру
    eligibility_list = list_to_lower(eligibility_list)  # приводим все кошельки к нижнему регистру

    wallets_with_drop = []  # список кошельков, которые получили дроп
    wallets_status = []  # список всех кошельков с проставленным статусом, получил дроп или нет

    for wallet in wallets:
        if wallet in eligibility_list:  # проверяем наличие кошелька в списке кошельков, которые получили дроп
            wallets_with_drop.append(wallet)  # добавляем кошелек в список кошельков, которые получили дроп
            print(f"{wallet}-ELIGIBLE")  # выводим на экран кошелек с проставленным статусом, получил дроп или нет
            wallets_status.append(f"{wallet}-ELIGIBLE")  # добавляем кошелек в список всех кошельков с проставленным статусом, получил дроп или нет
        else:
            wallets_status.append(f"{wallet}-NOT ELIGIBLE")  # добавляем кошелек в список всех кошельков с проставленным статусом, получил дроп или нет

    print(f"Количество кошельков, которые получили дроп: {len(wallets_with_drop)}")  # выводим количество кошельков, которые получили дроп
    print(f"Процент кошельков, которые получили дроп: {len(wallets_with_drop) / len(wallets) * 100}%")  # выводим процент кошельков, которые получили дроп

    # записываем список кошельков, которые получили дроп, в файл wallets_with_drop.txt
    write_list_to_file("data/wallets_with_drop.txt", wallets_with_drop)
    # записываем список всех кошельков с проставленным статусом, получил дроп или нет, в файл wallets_status.txt
    write_list_to_file("data/wallets_status.txt", wallets_status)



if __name__ == '__main__':
    main()

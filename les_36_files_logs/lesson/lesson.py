import random
import time


def main():
    # file = open("data/wallets.txt")
    # wallets_data = file.read().split("\n")
    # file.close()
    #
    # for wallet_with_balance in wallets_data:
    #     wallet, balance = wallet_with_balance.split(" ")
    # #     print(wallet, balance)
    # file = open("data/result.txt")
    # wallets_data = file.read()
    # file.close()
    #
    # file = open("data/result.txt", "w")
    # # file.write("Hello, World!")
    # my_list = [1, 2, 3, 4, 5]
    # for el in my_list:
    #     file.write(str(el) + "\n")

    # file = open("data/result.txt")
    # wallets_data = file.read()
    # file.close()
    #
    # file = open("data/result.txt", "w")
    # text = wallets_data + "сообщение 2"
    # file.write(text + "\n")
    # file.close()
    # file = open("data/result.txt", "a")
    # file.write("сообщение 5" + "\n")
    # file.close()
    # file = open("data/wallets.txt")
    # wallets = file.read().split("\n")
    # file.close()
    #
    #
    #
    #
    # for wallet in wallets:
    #     amount = random.randint(1, 100)
    #     file = open("data/result.txt", "a")
    #     file.write(f"{wallet}-{amount}\n")
    #     file.close()
    # print(f"Вывели токены на кошелек {wallet}, количество {amount}")
    #     time.sleep(3)


    with open("data/wallets.txt") as f:
        wallets = f.read().split("\n")
    print(wallets)

    for wallet in wallets:
        amount = random.randint(1, 100)
        with open("data/result.txt", "a") as f:
            f.write(f"{wallet}-{amount}\n")

        print(f"Вывели токены на кошелек {wallet}, количество {amount}")


    # обработка данных




if __name__ == '__main__':
    main()
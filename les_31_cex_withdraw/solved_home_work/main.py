import functions

def main():

    okx_tokens = functions.get_okx_tokens() # Получаем список токенов с биржи okx
    for i, token in enumerate(okx_tokens): # Перебираем список токенов
        print(f"okx: {i} {token}") # Выводим токен

    binance_tokens = functions.get_binance_tokens() # Получаем список токенов с биржи binance
    for i, token in enumerate(binance_tokens): # Перебираем список токенов
        print(f"binance: {i} {token}") # Выводим токен

if __name__ == "__main__":
    main()

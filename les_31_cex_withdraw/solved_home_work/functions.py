import ccxt

def get_okx_tokens():
    okx = ccxt.okx()  # Создаем объект подключения к бирже
    tokens_data = okx.fetch_markets()  # Получаем данные о торговых парах
    token_pairs = [token_data["symbol"] for token_data in tokens_data]  # Получаем список торговых пар
    return token_pairs  # Возвращаем список торговых пар


def get_binance_tokens():
    binance = ccxt.binance()  # Создаем объект подключения к бирже
    tokens_data = binance.fetch_markets()  # Получаем данные о торговых парах
    token_pairs = [token_data["symbol"] for token_data in tokens_data]  # Получаем список торговых пар
    return token_pairs  # Возвращаем список торговых пар

""""""

""" 
Реализовать функцию:

    def shuffle_private_key(private_key: str) -> str:
        pass


Функция shuffle_private_key должна принимать закрытый ключ private_key 
и перемешивать его символы по пин-коду из конфига.

"""


def shuffle_private_key(private_key: str) -> str:
    pin_pairs = pin_pk.split(" ")
    private_key = list(private_key)
    for pair in pin_pairs:
        first_index, second_index = pair.split("-")
        first_index, second_index = int(first_index), int(second_index)
        private_key[first_index], private_key[second_index] = private_key[second_index], private_key[first_index]

    return " ".join(seed)
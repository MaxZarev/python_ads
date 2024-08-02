import random
import secrets
import string
import time

from config import salt, pin, pin_seed

def shuffle_seed(seed: str) -> str:
    pin_pairs = pin_seed.split(" ")
    seed = seed.split(" ")
    for pair in pin_pairs:
        first_index, second_index = pair.split("-")
        first_index, second_index = int(first_index), int(second_index)
        seed[first_index], seed[second_index] = seed[second_index], seed[first_index]
    with open("bep39.txt") as file:
        words = file.read().splitlines()

    first_index, second_index = pin_pairs[0].split("-")
    first_index, second_index = int(first_index), int(second_index)

    seed.insert(first_index, secrets.choice(words))
    seed.insert(second_index, secrets.choice(words))
    return " ".join(seed)

def unshuffle_seed(seed: str) -> str:
    pin_pairs = pin_seed.split(" ")
    seed = seed.split(" ")

    first_index, second_index = pin_pairs[0].split("-")
    first_index, second_index = int(first_index), int(second_index)

    seed.pop(second_index)
    seed.pop(first_index)

    for pair in pin_pairs:
        first_index, second_index = pair.split("-")
        first_index, second_index = int(first_index), int(second_index)
        seed[first_index], seed[second_index] = seed[second_index], seed[first_index]
    return " ".join(seed)


def get_list_from_file(path: str) -> list[str]:
    """
    Get list from file
    :param path: название файла
    :return: список строк из файла
    """
    with open(path, "r") as file:
        return file.read().splitlines()

def sleep_random(min_delay: float = 0.5, max_delay: float = 1.5) -> None:
    """
    Sleep random time
    :param min_delay: минимальное время задержки
    :param max_delay: максимальное время задержки
    :return: время задержки
    """
    delay = random.uniform(min_delay, max_delay)  # Генерируем случайное число
    time.sleep(delay)  # Делаем перерыв

def generate_password(length_min: int = 25, length_max: int = 35) -> str:
    """
    Generate password
    :param length_min:
    :param length_max:
    :return:
    """
    length = random.randint(length_min, length_max)  # Генерируем случайную длину пароля

    # Определяем наборы символов
    all_characters = [string.ascii_uppercase, string.ascii_uppercase, string.digits, string.punctuation]

    # Обеспечиваем наличие хотя бы одного символа каждого типа
    password = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation)
    ]

    while len(password) < length:
        characters = secrets.choice(all_characters)
        password.append(secrets.choice(characters))

    # Перемешиваем пароль, чтобы сделать его менее предсказуемым
    random.shuffle(password)

    return ''.join(password)


def write_text_to_file(path: str, text: str) -> None:
    """
    Write string to file
    :param path: название файла
    :param text: текст
    """
    with open(path, "a") as file:
        file.write(text + "\n")

def salt_password(password: str) -> str:
    return password + salt

def shuffle_password(password: str) -> str:
    pin_pairs = pin.split(" ")
    password = list(password)
    for pair in pin_pairs:
        first_index, second_index = pair.split("-")
        first_index, second_index = int(first_index), int(second_index)
        password[first_index], password[second_index] = password[second_index], password[first_index]

    return "".join(password)

if __name__ == '__main__':

    seed = "super impose give glimpse food initial artist figure loop jazz today cruel"
    print(seed)
    shuffled_seed = shuffle_seed(seed)
    print(shuffled_seed)
    unshuffled_seed = unshuffle_seed(shuffled_seed)
    print(unshuffled_seed)


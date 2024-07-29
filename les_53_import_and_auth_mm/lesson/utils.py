import random
import string
import time


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
    all_characters = string.ascii_letters + string.digits + string.punctuation

    # Обеспечиваем наличие хотя бы одного символа каждого типа
    password = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]

    # Заполняем оставшиеся символы случайными символами из полного набора
    password += random.choices(all_characters, k=length - 4)

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

""""""
import random

"""
Создать проект нагуливатель Куки.
Скрипт должен брать текстовый файл с перечисленными номерами профилей.
Скрипт должен брать текстовый файл с топ 100 популярных сайтов для нагуливания куки.
Скрипт должен запускать в рандомном порядке профили, брать рандомный сайт и заходить на него на 5-10 секунд.
Каждый профиль должен открыть 3-4 рандомных сайта из списка.
"""

import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def get_list_from_file(file_name: str) -> list:
    """
    Читает файл и возвращает список строк
    :param file_name: имя файла с расширением
    :return: список строк
    """
    with open(file_name, "r") as file:
        return file.read().splitlines()


def start_profile(profile_number: int) -> webdriver.Chrome:
    """
    Запускает профиль в браузере adspower и возвращает драйвер
    :param profile_number: номер профиля
    :return: драйвер
    """
    profile_data = _open_browser(profile_number)
    if profile_data:
        chrome_driver = profile_data["data"]["webdriver"]
        selenium_port = profile_data["data"]["ws"]["selenium"]

        service = Service(executable_path=chrome_driver)

        options = Options()
        options.add_experimental_option("debuggerAddress", selenium_port)
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(options=options, service=service)
        return driver


def close_browser(profile_number: int) -> bool:
    """
    Закрывает профиль в браузере adspower по номеру профиля
    :param profile_number:  номер профиля
    :return:  True если успешно закрылся, иначе False
    """
    url = "http://local.adspower.net:50325/api/v1/browser/stop"
    parameters = {"serial_number": profile_number}
    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        return True
    else:
        return False


def _open_browser(profile_number: int):
    """
    Открывает профиль в браузере adspower по номеру профиля и возвращает данные профиля для инициализации драйвера
    :param profile_number: номер профиля
    :return: данные профиля для инициализации драйвера
    """
    url = "http://local.adspower.net:50325/api/v1/browser/start"
    parameters = {"serial_number": profile_number, "open_tabs": 1}
    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        return response.json()


def random_sleep(min_time: float = 5, max_time: float = 10) -> None:
    """
    Делает рандомную паузу от min_time до max_time
    :param min_time: минимальное время паузы
    :param max_time: максимальное время паузы
    :return: None
    """
    time.sleep(random.uniform(min_time, max_time))


def main():
    profiles = get_list_from_file("profiles.txt")  # список профилей
    sites = get_list_from_file("sites.txt")  # список сайтов
    for num_profile in profiles:  # проходим по профилям
        client = start_profile(num_profile)  # открываем профиль
        attempts = random.randint(3, 5)  # количество попыток
        for _ in range(attempts):  # проходим по попыткам
            site = random.choice(sites)  # выбираем рандомный сайт
            client.get(site)  # заходим на сайт
            random_sleep()  # делаем рандомную паузу
        close_browser(num_profile)  # закрываем профиль
        random_sleep(3, 5)  # делаем рандомную паузу


if __name__ == '__main__':
    main()

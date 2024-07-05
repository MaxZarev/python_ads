""""""
import random

from selenium.webdriver.common.by import By

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


def write_text_to_file(file_name: str, text: str) -> None:
    """
    Записывает текст в конец файла
    :param file_name: имя файла с расширением
    :param text: текст для записи
    :return: None
    """
    with open(file_name, "a") as file:
        file.write(text + "\n")


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


def sleep_random(min_time: float = 5, max_time: float = 10) -> None:
    """
    Делает рандомную паузу от min_time до max_time
    :param min_time: минимальное время паузы
    :param max_time: максимальное время паузы
    :return: None
    """
    time.sleep(random.uniform(min_time, max_time))


def parse_text(client: webdriver.Chrome, name_link: str) -> None:
    """
    Парсит текст и записывает его в файл
    :param text: текст
    :return: список строк
    """
    path = "result.txt"
    write_text_to_file(path, name_link)
    text_elements = client.find_elements(By.TAG_NAME, "p")
    for text_element in text_elements:
        write_text_to_file(path, text_element.text)


def open_menu(client: webdriver.Chrome, menu_names: list) -> None:
    """
    Раскрывает все пункты меню
    :param client: драйвер
    :param menu_names: список пунктов меню
    :return: None
    """
    for menu_item in menu_names:
        sleep_random(0.1, 0.2)
        client.find_element(By.LINK_TEXT, menu_item).click()


def main():
    profile_number = 947
    menu_names = ["Overview", "Browser", "Groups", "Extensions", "Profiles", "Parameter Object", "Appendix"]  # список пунктов меню
    excluded_link_names = menu_names.copy()  # копируем список пунктов меню
    excluded_link_names.extend(["Powered by", "Official Home", "Sign up", "Download"])  # список ссылок которые нужно исключить

    client = start_profile(profile_number)  # открываем профиль
    client.get("https://localapi-doc-en.adspower.com/docs/overview")  # заходим на сайт
    sleep_random()  # делаем рандомную паузу
    open_menu(client, menu_names)  # раскрываем всю меню
    all_links = client.find_elements(By.TAG_NAME, "a")  # находим все ссылки на странице
    links_name = []
    for link in all_links:
        if link.text:  # если есть текст в ссылке
            if link.text not in excluded_link_names:  # если текста нет в исключенных ссылках
                links_name.append(link.text)  # добавляем текст в список

    for link_name in links_name:  # проходим по всем ссылкам
        client.find_element(By.LINK_TEXT, link_name).click()  # кликаем по ссылке
        sleep_random(1, 3)
        parse_text(client, link_name)
        sleep_random(1, 3)

    sleep_random()
    close_browser(profile_number)  # закрываем профиль
    sleep_random(3, 5)  # делаем рандомную паузу


if __name__ == '__main__':
    main()

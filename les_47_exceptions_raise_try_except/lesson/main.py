from __future__ import annotations

import json
import random
import time
from pprint import pprint

import requests
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def filter_tabs(driver: webdriver.Chrome):
    """
    Фильтрует табы и возвращает список табов, которые не являются "Rabby Offscreen Page"
    :param driver:  драйвер браузера
    :return:  список табов за исключением перечисленных
    """
    start_tabs = driver.window_handles
    final_tabs = []
    for tab in start_tabs:
        driver.switch_to.window(tab)
        if driver.name != "Rabby Offscreen Page":
            final_tabs.append(tab)

    return final_tabs


def prepare_browser(driver: webdriver.Chrome):
    """
    Закрывать лишние вкладки кроме одной и разворачивать окно на весь экран
    :param driver:
    :return: None
    """

    tabs = filter_tabs(driver)

    if len(tabs) > 1:
        for tab in tabs[1:]:
            driver.switch_to.window(tab)
            driver.close()

    driver.switch_to.window(tabs[0])
    driver.maximize_window()


def get_list_from_file(path: str) -> list[str]:
    """
    Get list from file
    :param path: название файла
    :return: список строк из файла
    """
    with open(path, "r") as file:
        return file.read().splitlines()


def check_proxy(driver: webdriver.Chrome, proxy: str) -> bool:
    """
    Check proxy status
    :param driver: драйвер браузера
    :param proxy: прокси http в формате "ip:port:login:password"
    :return: True если прокси работает, False если нет
    """
    ip, port, login, password = proxy.split(":")
    current_ip = get_ip(driver)
    return current_ip == ip


def check_browser(profile_number: int) -> dict:
    """
    Check browser status and return data dict
    :param profile_number:  номер профиля в адс
    :return:  dict with browser data
    """
    url = "http://local.adspower.net:50325/api/v1/browser/active"
    parameters = {"serial_number": profile_number}
    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        return response.json()


def get_profile_id(profile_number: int) -> str:
    """
    Get profile id by profile number
    :param profile_number:
    :return: ads profile id
    """
    url = "http://local.adspower.net:50325/api/v1/user/list"
    parameters = {"serial_number": profile_number}
    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        return response.json()['data']['list'][0]['user_id']


def set_proxy(profile_number: int, proxy: str) -> bool:
    """
    Set proxy for profile
    :param profile_number: номер профиля в адс
    :param proxy: прокси http в формате "ip:port:login:password"
    :return:
    """
    ip, port, login, password = proxy.split(":")

    profile_id = get_profile_id(profile_number)

    proxy_config = {
        "proxy_type": "http",
        "proxy_host": ip,
        "proxy_port": port,
        "proxy_user": login,
        "proxy_password": password,
        "proxy_soft": "other"
    }

    data = {
        "user_id": profile_id,
        "user_proxy_config": proxy_config
    }
    url = "http://local.adspower.net:50325/api/v1/user/update"
    response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
    if response.status_code == 200:
        return True
    else:
        return False


def start_profile(profile_number: int, proxy: str = "") -> webdriver.Chrome:
    """
    Проверяет запущен ли браузер, если нет - запускает, и подключает Селениум к браузеру, возвращает инстанс браузера
    :param proxy:
    :param profile_number: номер профиля в адс
    :return: инстанс браузера по номеру профиля
    """
    if proxy:
        set_proxy(profile_number, proxy)

    profile_data = check_browser(profile_number)  # проверяем статус браузера по номеру профиля и получаем данные
    if profile_data["data"]["status"] != "Active":  # если браузер не активен запускаем браузер
        profile_data = open_browser(profile_number)  # запускаем браузер и получаем данные

    if profile_data:
        chrome_driver = profile_data["data"]["webdriver"]
        selenium_port = profile_data["data"]["ws"]["selenium"]

        service = Service(executable_path=chrome_driver)

        options = Options()
        options.add_experimental_option("debuggerAddress", selenium_port)
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(options=options, service=service)

        if proxy:
            if not check_proxy(driver, proxy):
                raise Exception("Proxy is not work")

        prepare_browser(driver)
        return driver


def close_browser(driver: webdriver.Chrome, profile_number: int):
    """
    Закрываем браузер силами Селениума, если не закрылся отправляем запрос на закрытие браузера в АДС, с проверкой статуса
    :param driver: драйвер браузера
    :param profile_number: номер профиля в адс
    :return:
    """
    driver.close()
    for _ in range(3):
        time.sleep(5)
        data = check_browser(profile_number)
        if data["data"]["status"] == "Active":
            url = "http://local.adspower.net:50325/api/v1/browser/stop"
            parameters = {"serial_number": profile_number}
            requests.get(url, params=parameters)
        else:
            break


def open_browser(profile_number: int) -> dict:
    """
    Open browser
    :param profile_number:  номер профиля в адс
    :return:  dict with browser data
    """
    url = "http://local.adspower.net:50325/api/v1/browser/start"
    parameters = {"serial_number": profile_number, "open_tabs": 1, "ip_tab": 1}
    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        return response.json()


def get_ip(driver: webdriver.Chrome) -> str:
    """
    Get current ip
    :param driver: драйвер браузера
    :return: ip адрес браузера
    """
    url = "https://api.ipify.org/?format=json"
    tab = driver.window_handles[0]
    driver.switch_to.window(tab)
    driver.get(url)
    time.sleep(1)
    current_ip_data = driver.find_element(By.TAG_NAME, "pre").text  # получаем текст из тега pre
    return json.loads(current_ip_data)["ip"]  # парсим json и возвращаем ip


def sleep_random(min_delay: float = 0.5, max_delay: float = 1.5) -> None:
    """
    Sleep random time
    :param min_delay: минимальное время задержки
    :param max_delay: максимальное время задержки
    :return: время задержки
    """
    delay = random.uniform(min_delay, max_delay)  # Генерируем случайное число
    time.sleep(delay)  # Делаем перерыв


def find_element(driver: webdriver.Chrome, xpath: str) -> WebElement | None:
    try:
        return driver.find_element(By.XPATH, xpath)
    except NoSuchElementException:
        print(f"Element not found by xpath: {xpath}")
        return None

def click_element(driver: webdriver.Chrome, xpath: str) -> bool:
    web_element = find_element(driver, xpath)
    if web_element:
        web_element.click()
        return True
    else:
        return False


def main():
    profiles = [590, 591, 592, 593, 594, 595, 596, 597, 598, 599]
    for profile in profiles:
        driver = start_profile(profile)  # запускаем профиль по номеру, без прокси
        try:
            driver.get("https://pancakeswap.finance/swap")  # открываем сайт
            click_element(driver, "//button[contains(text(), 'Connect')]")
            print("какая-то логика")
            sleep_random(5, 10)
        except Exception as error:
            print(error)
            # добавьте код тут
        finally:
            close_browser(driver, profile)  # закрываем браузер


if __name__ == '__main__':
    main()

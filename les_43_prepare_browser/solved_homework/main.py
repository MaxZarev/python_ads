import json
import time
from pprint import pprint

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def get_list_from_file(path: str) -> list[str]:
    """
    Get list from file
    :param path: название файла
    :return: список строк из файла
    """
    with open(path, "r") as file:
        return file.read().splitlines()


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


def set_proxy(profile_number: int, proxy: str):
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


def start_profile(profile_number: int) -> webdriver.Chrome:
    profile_data = open_browser(profile_number)
    if profile_data:
        chrome_driver = profile_data["data"]["webdriver"]
        selenium_port = profile_data["data"]["ws"]["selenium"]

        service = Service(executable_path=chrome_driver)

        options = Options()
        options.add_experimental_option("debuggerAddress", selenium_port)
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(options=options, service=service)
        return driver


def close_browser(profile_number: int):
    url = "http://local.adspower.net:50325/api/v1/browser/stop"
    parameters = {"serial_number": profile_number}
    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        return True
    else:
        return False


def open_browser(profile_number: int):
    url = "http://local.adspower.net:50325/api/v1/browser/start"
    parameters = {"serial_number": profile_number, "open_tabs": 1}
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
    driver.get(url)
    time.sleep(1)
    current_ip_data = driver.find_element(By.TAG_NAME, "pre").text  # получаем текст из тега pre
    return json.loads(current_ip_data)["ip"]  # парсим json и возвращаем ip


def main():
    profiles = get_list_from_file("profiles.txt")  # список номеров профилей
    proxies = get_list_from_file("proxies.txt")  # список прокси
    ips = get_list_from_file("ips.txt")  # список ip адресов

    for profile, proxy, ip in zip(profiles, proxies, ips):  # проходим по спискам одновременно
        profile_number = int(profile)  # преобразуем номер профиля в число
        set_proxy(profile_number, proxy)  # устанавливаем прокси
        time.sleep(5)  # ждем 5 секунд
        driver = start_profile(profile_number)  # запускаем профиль
        time.sleep(3)  # ждем 3 секунды
        current_ip = get_ip(driver)  # получаем текущий ip
        if current_ip == ip:  # сравниваем текущий ip с тем, что был взят из файла
            print(f"№ {profile_number} Success")
        else:
            print(f"№ {profile_number} Fail")
        close_browser(profile_number)


if __name__ == '__main__':
    main()

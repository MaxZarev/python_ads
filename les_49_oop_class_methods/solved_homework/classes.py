from __future__ import annotations

import json
import random
import time

import requests
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

class Ads:
    def __init__(self, profile_number: int, proxy: str = ""):
        self.profile_number: int = profile_number
        self.proxy: str = proxy
        self.set_proxy()
        self.driver: webdriver.Chrome = self.start_profile()
        self.prepare_browser()
        self.check_proxy()

    def filter_tabs(self) -> list[str]:
        """
        Фильтрует табы и возвращает список табов, которые не являются исключая скрытые табы
        :return: список табов
        """
        start_tabs = self.driver.window_handles
        final_tabs = []
        for tab in start_tabs:
            self.driver.switch_to.window(tab)
            if self.driver.name != "Rabby Offscreen Page":
                final_tabs.append(tab)

        return final_tabs


    def prepare_browser(self):
        """
        Закрывать лишние вкладки кроме одной и разворачивать окно на весь экран
        :return: None
        """

        tabs = self.filter_tabs()

        if len(tabs) > 1:
            for tab in tabs[1:]:
                self.driver.switch_to.window(tab)
                self.driver.close()

        self.driver.switch_to.window(tabs[0])
        self.driver.maximize_window()


    def get_list_from_file(self, path: str) -> list[str]:
        """
        Get list from file
        :param path: название файла
        :return: список строк из файла
        """
        with open(path, "r") as file:
            return file.read().splitlines()


    def check_proxy(self):
        """
        Проверяет прокси сравнивая ip адреса, если указаны при инициализации, если не работает - вызывает исключение,
        :return: None
        """
        if not self.proxy:
            return
        ip, port, login, password = self.proxy.split(":")
        current_ip = self.get_ip()
        if current_ip != ip:
            raise Exception("Proxy not working")


    def check_browser(self) -> dict:
        """
        Запрашивает статус браузера по номеру профиля
        :return: словарь с данными браузера
        """
        url = "http://local.adspower.net:50325/api/v1/browser/active"
        parameters = {"serial_number": self.profile_number}
        response = requests.get(url, params=parameters)
        response.raise_for_status()
        return response.json()


    def get_profile_id(self) -> str:
        """
        Получает id профиля по номеру профиля
        :return: id профиля
        """

        url = "http://local.adspower.net:50325/api/v1/user/list"
        parameters = {"serial_number": self.profile_number}
        response = requests.get(url, params=parameters)
        response.raise_for_status()
        return response.json()['data']['list'][0]['user_id']


    def set_proxy(self):
        """
        Устанавливает прокси для профиля, запускать до старта профиля
        :return
        """
        if not self.proxy:
            return

        ip, port, login, password = self.proxy.split(":")

        profile_id = self.get_profile_id()

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
        response.raise_for_status()



    def start_profile(self) -> webdriver.Chrome:
        """
        Проверяет запущен ли браузер, если нет - запускает, и подключает Селениум к браузеру, возвращает инстанс браузера
        :return: драйвер браузера
        """

        profile_data = self.check_browser()  # проверяем статус браузера по номеру профиля и получаем данные
        if profile_data["data"]["status"] != "Active":  # если браузер не активен запускаем браузер
            profile_data = self.open_browser()  # запускаем браузер и получаем данные

        if profile_data:
            chrome_driver = profile_data["data"]["webdriver"]
            selenium_port = profile_data["data"]["ws"]["selenium"]

            service = Service(executable_path=chrome_driver)

            options = Options()
            options.add_experimental_option("debuggerAddress", selenium_port)
            options.add_argument("--disable-blink-features=AutomationControlled")

            driver = webdriver.Chrome(options=options, service=service)

            return driver


    def close_browser(self):
        """
        Закрывает браузер и отправляет запрос на закрытие браузера в ADS
        :return: None
        """
        self.driver.close()
        for _ in range(3):
            time.sleep(5)
            data = self.check_browser()
            if data["data"]["status"] == "Active":
                url = "http://local.adspower.net:50325/api/v1/browser/stop"
                parameters = {"serial_number": self.profile_number}
                requests.get(url, params=parameters)
            else:
                break


    def open_browser(self) -> dict:
        """
        Отправляет запрос на открытие браузера в ADS
        :return: словарь с данными браузера
        """
        url = "http://local.adspower.net:50325/api/v1/browser/start"
        parameters = {"serial_number": self.profile_number, "open_tabs": 1}
        response = requests.get(url, params=parameters)
        if response.status_code == 200:
            return response.json()


    def get_ip(self) -> str:
        """
        Получает ip адрес текущего браузера
        :return: ip адрес
        """
        url = "https://api.ipify.org/?format=json"
        tab = self.driver.window_handles[0]
        self.driver.switch_to.window(tab)
        self.driver.get(url)
        self.sleep_random()
        current_ip_data = self.driver.find_element(By.TAG_NAME, "pre").text  # получаем текст из тега pre
        return json.loads(current_ip_data)["ip"]  # парсим json и возвращаем ip


    def sleep_random(self, min_delay: float = 0.5, max_delay: float = 1.5) -> None:
        """
        Sleep random time
        :param min_delay: минимальное время задержки
        :param max_delay: максимальное время задержки
        :return: None
        """
        delay = random.uniform(min_delay, max_delay)  # Генерируем случайное число
        time.sleep(delay)  # Делаем перерыв


    def find_element(self, xpath: str) -> WebElement | None:
        """
        Ищет веб элемент по xpath без вызова исключения в случае не нахождения
        :param xpath: xpath элемента
        :return:  веб элемент или None
        """
        try:
            return self.driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            print(f"Element not found by xpath: {xpath}")
            return None


    def click_element(self, xpath: str) -> bool:
        """
        Кликает на элемент по xpath без вызова исключения в случае не нахождения
        :param xpath: xpath элемента
        :return: True если кликнули, False если нет
        """
        web_element = self.find_element(xpath)
        if web_element:
            web_element.click()
            return True
        else:
            return False

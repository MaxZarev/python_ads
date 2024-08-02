from __future__ import annotations

import json
import time

from classes.excel import Excel
from utils import sleep_random
import requests
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from config import set_proxy, check_proxy


class Ads:

    def __init__(self, profile_number: int, proxy: str = ""):
        self.profile_number: int = profile_number
        self.proxy: str = proxy
        if set_proxy:
            self._set_proxy()
        self.driver: webdriver.Chrome = self._start_profile()
        self._prepare_browser()
        if check_proxy:
            self._check_proxy()
        self.excel = Excel("wallets.xlsx")



    def _start_profile(self) -> webdriver.Chrome:

        profile_data = self._check_browser()  # проверяем статус браузера по номеру профиля и получаем данные
        if profile_data["data"]["status"] != "Active":  # если браузер не активен запускаем браузер
            profile_data = self._open_browser()  # запускаем браузер и получаем данные

        chrome_driver = profile_data["data"]["webdriver"]
        selenium_port = profile_data["data"]["ws"]["selenium"]

        service = Service(executable_path=chrome_driver)

        options = Options()
        options.add_experimental_option("debuggerAddress", selenium_port)
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(options=options, service=service)
        return driver

    def _check_browser(self) -> dict:
        url = "http://local.adspower.net:50325/api/v1/browser/active"
        parameters = {"serial_number": self.profile_number}
        response = requests.get(url, params=parameters)
        response.raise_for_status()
        return response.json()

    def _open_browser(self) -> dict:
        url = "http://local.adspower.net:50325/api/v1/browser/start"
        parameters = {"serial_number": self.profile_number, "open_tabs": 1}
        response = requests.get(url, params=parameters)
        response.raise_for_status()
        return response.json()

    def _set_proxy(self) -> None:
        ip, port, login, password = self.proxy.split(":")

        profile_id = self._get_profile_id()

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

    def _get_profile_id(self) -> str:
        url = "http://local.adspower.net:50325/api/v1/user/list"
        parameters = {"serial_number": self.profile_number}
        response = requests.get(url, params=parameters)
        response.raise_for_status()
        return response.json()['data']['list'][0]['user_id']

    def _prepare_browser(self):
        sleep_random(3, 4)
        tabs = self._filter_tabs()

        if len(tabs) > 1:
            for tab in tabs[1:]:
                self.driver.switch_to.window(tab)
                self.driver.close()

        self.driver.switch_to.window(tabs[0])
        self.driver.maximize_window()

    def _filter_tabs(self):
        start_tabs = self.driver.window_handles
        final_tabs = []
        for tab in start_tabs:
            self.driver.switch_to.window(tab)
            if self.driver.name != "Rabby Offscreen Page":
                final_tabs.append(tab)

        return final_tabs

    def _check_proxy(self):
        ip, port, login, password = self.proxy.split(":")
        current_ip = self._get_ip()
        if current_ip != ip:
            raise Exception("Прокси не работает")

    def _get_ip(self):
        tab = self.driver.window_handles[0]
        self.driver.switch_to.window(tab)
        try:
            self.driver.get("https://api.ipify.org/?format=json")
            time.sleep(1)
            web_el = self.find_element("//pre")
            ip = json.loads(web_el.text)["ip"]  # парсим json и возвращаем ip
        except Exception:
            self.driver.get("https://start.adspower.net/")
            time.sleep(2)
            web_el = self.find_element("//span[starts-with(@class, '_header__ip')]")
            if not web_el:
                raise Exception("Не удалось получить ip")
            ip = web_el.text

        return ip

    def close_browser(self):
        self.driver.close()
        for _ in range(3):
            time.sleep(5)
            data = self._check_browser()
            if data["data"]["status"] == "Active":
                url = "http://local.adspower.net:50325/api/v1/browser/stop"
                parameters = {"serial_number": self.profile_number}
                requests.get(url, params=parameters)
            else:
                break

    def find_element(self, xpath: str, timeout: int = 15) -> WebElement | None:
        """
        Ищет элемент по xpath на странице, делает несколько попыток с рандомной паузой от 0.9 до 1.2 секунды
        :param xpath: xpath элемента
        :param timeout: количество попыток найти элемент
        :return: элемент или None
        """
        # Пытаемся найти элемент на странице заданное количество раз
        for attempt in range(timeout):
            # Пытаемся найти элемент на странице, если не найден, ловим исключение
            try:
                # Возвращаем элемент, если он найден
                return self.driver.find_element(By.XPATH, xpath)
            except NoSuchElementException:
                # Если это не последняя попытка, делаем паузу
                sleep_random(0.9, 1.2)
        # Если элемент не найден за указанное время, возвращаем None
        return None

    def get_text(self, xpath: str, timeout: int = 15) -> str:
        """
        Получает текст элемента по xpath, делает несколько попыток с рандомной паузой от 0.9 до 1.2 секунды. Если элемент не найден, возвращает пустую строку.
        :param xpath: xpath элемента
        :param timeout: количество попыток найти элемент
        :return: текст элемента или пустая строка
        """
        # Ищем элемент на странице
        web_element = self.find_element(xpath, timeout)
        # Возвращаем текст элемента, если он найден, иначе пустую строку
        return web_element.text if web_element else ""

    def input_text(self, xpath: str, text: str, timeout: int = 15) -> bool:
        web_element = self.find_element(xpath, timeout)
        if web_element:
            web_element.send_keys(text)
            return True
        else:
            return False

    def click_element(self, xpath: str,  timeout: int = 15) -> bool:
        web_element = self.find_element(xpath, timeout)
        if web_element:
            web_element.click()
            return True
        else:
            return False

    def open_url(self, url: str, xpath: str = "", timeout: int = 15):
        """
        Открывает страницу в браузере, если она еще не открыта, валидирует ссылку, если не хватает http:// или https://, добавляет http://,
        если передан xpath, то ждет элемент на странице заданное время
        :param url: ссылка
        :param xpath: xpath элемента
        :param timeout: количество попыток найти элемент
        """

        # Проверяем, если передана ссылка на расширение chrome
        if url.startswith("chrome-extension"):
            if self.driver.current_url == url:
                return

            self.driver.get(url)


        # Проверяем и добавляем http:// или https:// если необходимо
        if not url.startswith("http://") and not url.startswith("https://"):
            http_url = f"http://{url}"
            https_url = f"https://{url}"
        else:
            http_url = url
            https_url = ""

        # Проверяем, если одна из версий URL уже открыта
        if self.driver.current_url in [http_url, https_url, url]:
            return

        # Пытаемся открыть http версию URL
        self.driver.get(http_url)

        # Если передан xpath, ждем элемент на странице заданное время
        if xpath:
            self.find_element(xpath, timeout)


if __name__ == '__main__':
    try:
        ads = Ads(749, "185.149.21.78:3000:jINV9g:DXqi8PtrAp")
        ads.open_url("google.com")
        ads.open_url("google.com")
        sleep_random(5, 10)
        ads.close_browser()
        text = ads.get_text("//span")
    except Exception as ex:

        print(ex)

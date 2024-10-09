from __future__ import annotations

import json
import random
from typing import Optional, Literal

import requests

from config import link_change_ip, is_mobile_proxy, set_proxy, check_proxy
from utils import random_sleep, get_response

from playwright.sync_api import sync_playwright, Browser, Page, Locator


class Ads:
    local_api_url = "http://local.adspower.net:50325/api/v1/"

    def __init__(self, profile_number: int, proxy: Optional[str] = None):
        self.proxy = proxy
        self.profile_number = profile_number
        if set_proxy:
            self._set_proxy()
        self.browser = self._start_browser()
        self.context = self.browser.contexts[0]
        self.page = self.context.new_page()
        self._prepare_browser()

        if is_mobile_proxy:
            get_response(link_change_ip, attempts=1, return_except=False)

        if check_proxy:
            self._check_proxy()

    def _open_browser(self) -> str:
        """
        Открывает браузер в ADS по номеру профиля
        :return: параметры запущенного браузера
        """

        params = dict(serial_number=self.profile_number)
        url = self.local_api_url + 'browser/start'
        random_sleep(1, 2)
        try:
            data = get_response(url, params)
            return data['data']['ws']['puppeteer']
        except Exception as e:
            print(f"{self.profile_number}: Ошибка при открытии браузера: {e}")
            raise e

    def _check_browser_status(self) -> Optional[str]:
        """
        Проверяет статус браузера в ADS по номеру профиля
        :return: параметры запущенного браузера
        """
        params = dict(serial_number=self.profile_number)
        url = self.local_api_url + 'browser/active'
        random_sleep(1, 2)
        try:
            data = get_response(url, params)
            if data['data']['status'] == 'Active':
                print(f"{self.profile_number}: Браузер уже активен")
                return data['data']['ws']['puppeteer']
            return None
        except Exception as e:
            print(f"{self.profile_number}: Ошибка при проверке статуса браузера: {e}")
            raise e

    def _start_browser(self) -> Browser:
        """
        Запускает браузер в ADS по номеру профиля.
        Делает 3 попытки прежде чем вызвать исключение.
        :return: Browser
        """
        for attempt in range(3):
            try:
                # Проверяем статус браузера и запускаем его, если не активен
                if not (endpoint := self._check_browser_status()):
                    print(f"{self.profile_number}: Запускаем браузер")
                    random_sleep(3, 4)
                    endpoint = self._open_browser()

                # подключаемся к браузеру
                random_sleep(4, 5)
                pw = sync_playwright().start()
                slow_mo = random.randint(800, 1200)
                browser = pw.chromium.connect_over_cdp(endpoint, slow_mo=slow_mo)
                if browser.is_connected():
                    return browser
                print(f"{self.profile_number}: Error не удалось запустить браузер")

            except Exception as e:
                print(f"{self.profile_number}: Error не удалось запустить браузер {e}")
                random_sleep(5, 10)

        raise Exception(f"{self.profile_number}: Error не удалось запустить браузер")

    def _prepare_browser(self) -> None:
        """
        Закрывает все страницы кроме текущей
        :return: None
        """
        try:
            for page in self.context.pages:
                page = page
                if 'offscreen' in page.url:
                    continue
                if page.url != self.page.url:
                    page.close()

        except Exception as e:
            print(f"{self.profile_number}: Ошибка при закрытии страниц: {e}")
            raise e

    def close_browser(self) -> None:
        """
        Останавливает браузер в ADS по номеру профиля
        :return: None
        """
        self.browser.close()
        params = dict(serial_number=self.profile_number)
        url = self.local_api_url + 'browser/stop'
        random_sleep(1, 2)
        try:
            get_response(url, params)
        except Exception as e:
            print(f"{self.profile_number} Ошибка при остановке браузера: {e}")
            raise e

    def catch_page(self, url_contains: str | list[str] = None, timeout: int = 10) -> \
            Optional[Page]:
        """
        Ищет страницу по частичному совпадению url.
        :param url_contains: текст, который ищем в url или список текстов
        :param timeout:  время ожидания
        :return: страница с нужным url или None
        """
        if isinstance(url_contains, str):
            url_contains = [url_contains]

        for attempt in range(timeout):
            for page in self.context.pages:
                for url in url_contains:
                    if url in page.url:
                        return page
                    if attempt and attempt % 5 == 0:
                        self.pages_context_reload()
                    random_sleep(1, 2)

        print(f"{self.profile_number} Ошибка страница не найдена: {url_contains}")
        return None

    def pages_context_reload(self):
        """
        Перезагружает контекст страниц
        :return: None
        """
        self.context.new_page()
        random_sleep(1, 2)
        for page in self.context.pages:
            if 'about:blank' in page.url:
                page.close()

    def _set_proxy(self) -> None:
        """
        Устанавливает прокси для профиля в ADS
        :return: None
        """
        try:
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
            url = self.local_api_url + "user/update"
            response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
            response.raise_for_status()
            random_sleep(2)

        except Exception as e:
            print(f"{self.profile_number} Ошибка при установке прокси: {e}")
            raise e

    def _get_profile_id(self) -> str:
        """
        Запрашивает id профиля в ADS по номеру профиля
        :return: id профиля в ADS
        """
        url = self.local_api_url + 'user/list'
        params = {"serial_number": self.profile_number}

        random_sleep(1, 2)
        try:
            data = get_response(url, params)
            return data['data']['list'][0]['user_id']
        except Exception as e:
            print(f"{self.profile_number} Ошибка при получении id профиля: {e}")
            raise e

    def _check_proxy(self) -> None:
        """
        Проверяет, что прокси работает, сравнивая ip профиля и прокси, вызывает исключение, если не совпадают
        :return: None
        """
        ip, port, login, password = self.proxy.split(":")
        current_ip = self._get_ip()
        print(f"{self.profile_number} Текущий ip: {current_ip}")
        if current_ip != ip:
            raise Exception("Прокси не работает")

    def _get_ip(self) -> str:
        """
        Получает ip текущего профиля
        :return: ip
        """
        try:
            ip = self.page.evaluate('''
                        async () => {
                            const response = await fetch('https://api.ipify.org');
                            const data = await response.text();
                            return data;
                        }
                    ''')
        except Exception:
            print(f"{self.profile_number} Ошибка при получении ip")
            self.page.goto("https://api.ipify.org/?format=json")
            random_sleep(1, 2)
            ip_text = self.page.locator("//pre").inner_text()  # парсим json и возвращаем ip
            ip = json.loads(ip_text)["ip"]  # парсим json и возвращаем ip

        return ip

    def open_url(
            self,
            url: str,
            wait_until: Optional[
                Literal["commit", "domcontentloaded", "load", "networkidle"]
            ] = "load",
            locator: Optional[Locator] = None,
            timeout: int = 30,
            attempts: int = 1
    ) -> None:
        """
        Открывает страницу по url, если еще не открыта
        :param url: ссылка на страницу
        :param wait_until: состояние страницы, когда считается что она загрузилась
        :param locator: элемент, который нужно дождаться
        :param timeout: время ожидания в секундах
        :param attempts: количество попыток
        :return: None
        """
        # Переводим время ожидания в миллисекунды, если передали секунды
        if timeout < 1000:
            timeout = timeout * 1000

        # Проверяем, если передана ссылка на расширение chrome
        if not url.startswith("chrome-extension"):
            # Проверяем и добавляем https:// если необходимо
            if not (url.startswith("http://") or url.startswith("https://")):
                url = f"https://{url}"

        # Проверяем, если одна из версий URL уже открыта
        if self.page.url != url:
            for attempt in range(attempts):
                try:
                    self.page.goto(url, wait_until=wait_until, timeout=timeout)
                    break
                except Exception as e:
                    if attempt == attempts - 1:
                        raise e
                    print(f"{self.profile_number}: Ошибка при открытии страницы {url}: {e}")
                    random_sleep(1, 2)

        # Если передан xpath, ждем элемент на странице заданное время
        if locator:
            locator.wait_for(state='visible', timeout=timeout)

    def click_if_exists(
            self,
            locator: Optional[Locator] = None,
            *,
            method: Optional[Literal["test_id", "role", "text"]] = None,
            value: Optional[str] = None
    ) -> None:
        """
        Кликает по элементу, если он существует, можно передать локатор или метод поиска и имя элемента
        :param locator: локатор элемента
        :param method: метод поиска элемента
        :param name: value для поиска элемента, если role, в формате "role:name"
        :return:
        """
        if not locator:
            match method:
                case "test_id":
                    locator = self.page.get_by_test_id(value)
                case "role":
                    role, name = value.split(":", 1)
                    locator = self.page.get_by_role(role, name=name)
                case "text":
                    locator = self.page.get_by_text(value)

        if locator.count():
            locator.click()

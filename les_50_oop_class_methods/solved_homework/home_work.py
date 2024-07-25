""""""

""" 
Реализовать метод у класса Ads:

def get_text(self, xpath: str) -> str:
    принимает на вход xpath элемента, возвращает текст элемента, ищет элемент используя метод find_element

def open_url(self, url: str):
    принимает на вход url, открывает страницу в браузере
    валидирует ссылку, если не хватает http:// или https://, добавляет http://

Улучшить метод find_element:
добавить входной параметр timeout: int = 15, который будет отвечать за время ожидания элемента
метод должен делать указанное количество попыток найти элемент с рандомной паузой от 0.9 до 1.2 секунды
если элемент не найден за указанное время, возвращать None, если найден - возвращать элемент

"""
from __future__ import annotations

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


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

def open_url(self, url: str, xpath: str="", timeout: int = 15):
    """
    Открывает страницу в браузере, если она еще не открыта, валидирует ссылку, если не хватает http:// или https://, добавляет http://,
    если передан xpath, то ждет элемент на странице заданное время
    :param url: ссылка
    :param xpath: xpath элемента
    :param timeout: количество попыток найти элемент
    """

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



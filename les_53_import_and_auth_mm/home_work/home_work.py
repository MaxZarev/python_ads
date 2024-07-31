""""""

""" 
Реализовать метод у класса Metamask:

    def select_network(self, chain: str):
        pass
    
    def add_network(self, chain: str):
        pass
    
Метод select_network должен выбирать сеть в MetaMask, если ее нет, то добавлять через метод add_network.
Метод add_network должен добавлять сеть в MetaMask, берет данные из словаря chains в классе Metamask.
"""

from classes.ads import Ads
from utils import sleep_random, generate_password


class Metamask:
    chains = {
        "Binance Smart Chain": {
            "Network name": "Binance Smart Chain",
            "New RPC URL": "https://1rpc.io/bnb",
            "Chain ID": 56,
            "Currency Symbol": "BNB",
        },
    }

    def __init__(self, ads, password: str = None, seed: str = None):
        self._url = "chrome-extension://kfffndnaofmhjgfjincifaloeplkongj/home.html#"
        self.ads: Ads = ads
        self.password = password
        self.seed = seed

    def select_network(self, chain: str):
        """
        Выбирает сеть в metamask, если ее нет, то добавляет через метод add_network
        :param chain: Название сети
        :return:
        """
        # проверяем не выбрана ли уже нужная сеть
        if chain == self.ads.get_text("//button[@data-testid='network-display']/child::span"):
            return

        # открываем меню выбора сетей
        self.ads.click_element("//button[@data-testid='network-display']")

        # проверяем есть ли нужная сеть в списке
        if self.ads.find_element(f"//p[text()='{chain}']", 3):
            # если есть, то выбираем
            self.ads.click_element(f"//p[text()='{chain}']")
        else:
            # если нет, то добавляем
            self.ads.click_element("//button[text()='Add network']")
            self.add_network(chain)

    def add_network(self, chain: str):
        """
        Добавляет сеть в metamask, берет данные из словаря chains в классе Metamask
        :param chain:  Название сети
        :return:
        """

        # проверяем есть ли сеть в словаре
        if chain not in self.chains:
            raise ValueError(f"Добавьте '{chain}' в словарь chains в классе Metamask")

        # берем данные из словаря
        chain_name = self.chains[chain]["Network name"]
        rpc = self.chains[chain]["New RPC URL"]
        chain_id = str(self.chains[chain]["Chain ID"])
        currency = self.chains[chain]["Currency Symbol"]

        self.ads.open_url(self._url + "settings/networks/add-network")
        sleep_random(1, 3)

        # вводим данные в поля
        self.ads.input_text("//input[@data-testid='network-form-network-name']", chain_name)
        self.ads.input_text("//input[@data-testid='network-form-rpc-url']", rpc)

        self.ads.input_text("//input[@data-testid='network-form-chain-id']", chain_id)
        self.ads.input_text("//input[@data-testid='network-form-ticker-input']", currency)
        sleep_random(1, 3)
        # сохраняем и переключаемся на сеть
        self.ads.click_element("//button[text()='Save']")
        self.ads.click_element("//h6[contains(text(),'Switch to'"
                               ")]")

        self.ads.click_element("//button[@data-testid='popover-close']", 5)

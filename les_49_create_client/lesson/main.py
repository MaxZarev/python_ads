from ccxt import okx
# так что же такое класс?

from selenium import webdriver
from web3 import Web3


class ClientAds:
    def __init__(self, profile_number: int, proxy: str = ""):
        print("Создаем объект класса Ads")
        self.profile_number: int = profile_number
        self.proxy: str = proxy
        self.set_proxy()
        self.driver: webdriver.Chrome = self.open_browser()

    def open_browser(self) -> webdriver.Chrome:
        print(f"Отправляем запрос на открытия браузера в ADS с профилем {self.profile_number}")
        Ads.driver = "driver" + str(self.profile_number)
        return "driver"

    def set_proxy(self):
        if self.proxy:
            print(f"Отправляем запрос на устанавливаем прокси {self.proxy}")
        else:
            print("Прокси не установлен")

    def open_url(self, url: str):
        #self.driver.get(url)
        print(f"Открываем страницу {url} в браузере с профилем {self.profile_number}")

    def close_browser(self):
        # self.driver.quit()
        print(f"Закрываем браузер с профилем {self.profile_number} через драйвер")
        print(f"Отправляем запрос на закрытие браузера в ADS с профилем {self.profile_number}")

def main():

    client = ClientAds(777, "http://proxy.com")


























# class Ads:
#     profile_number = None
#     proxy = None
#     driver: webdriver.Chrome = None
#
#     def setup_ads(profile_number: int, proxy: str = ""):
#         Ads.profile_number = profile_number
#         Ads.proxy = proxy
#
#         Ads.set_proxy()
#         Ads.open_browser()
#
#     def open_browser():
#         print(f"Отправляем запрос на открытия браузера в ADS с профилем {Ads.profile_number}")
#         Ads.driver = "driver" + str(Ads.profile_number)
#
#     def set_proxy(class_object):
#         if class_object.proxy:
#             print(f"Отправляем запрос на устанавливаем прокси {class_object.proxy}")
#         else:
#             print("Прокси не установлен")
#
#     def open_url(url: str):
#         #Ads.driver.get(url)
#         print(f"Открываем страницу {url} в браузере с профилем {Ads.profile_number}")
#
#     def close_browser():
#         # Ads.driver.quit()
#         print(f"Закрываем браузер с профилем {Ads.profile_number} через драйвер")
#         print(f"Отправляем запрос на закрытие браузера в ADS с профилем {Ads.profile_number}")






if __name__ == '__main__':
    main()

# так что же такое класс?

from selenium import webdriver

class Ads:
    profile_number = None
    proxy = None
    driver: webdriver.Chrome = None

    def setup_ads(profile_number: int, proxy: str = ""):
        Ads.profile_number = profile_number
        Ads.proxy = proxy

        Ads.set_proxy()
        Ads.open_browser()

    def open_browser():
        print(f"Отправляем запрос на открытия браузера в ADS с профилем {Ads.profile_number}")
        Ads.driver = "driver" + str(Ads.profile_number)

    def set_proxy(class_object):
        if class_object.proxy:
            print(f"Отправляем запрос на устанавливаем прокси {class_object.proxy}")
        else:
            print("Прокси не установлен")

    def open_url(url: str):
        #Ads.driver.get(url)
        print(f"Открываем страницу {url} в браузере с профилем {Ads.profile_number}")

    def close_browser():
        # Ads.driver.quit()
        print(f"Закрываем браузер с профилем {Ads.profile_number} через драйвер")
        print(f"Отправляем запрос на закрытие браузера в ADS с профилем {Ads.profile_number}")


def main():
    ads_object = Ads()



if __name__ == '__main__':
    main()

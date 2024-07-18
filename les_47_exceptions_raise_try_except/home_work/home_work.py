""""""
import random

""" Доработайте код так, чтобы скрипт в случае возникновения исключения, 
вставал на рандомную паузу, а потом пробовал
повторить запуск того же профиля и выполнения логики скрипта,
Максимум 3 попытки. Если после 3 попыток скрипт не смог выполнить логику, 
переходит к следующему профилю.

Задание со звездочкой: попробуйте реализовать без использования цикла.
"""

def main():
    profiles = [590, 591, 592, 593, 594, 595, 596, 597, 598, 599]
    for profile in profiles:
        driver = start_profile(profile)  # запускаем профиль по номеру, без прокси
        try:
            driver.get("https://pancakeswap.finance/swap")  # открываем сайт
            click_element(driver, "//button[contains(text(), 'Connect')]")
            if random.choice([True, False]):
                raise Exception("exception")
            print("Профиль доработал", profile)
        except Exception as error:
            print(error, "профиль", profile)
        finally:
            close_browser(driver, profile)  # закрываем браузер
import json
import time
from pprint import pprint

import requests
from playwright.sync_api import sync_playwright


def open_browser(profile_number: int) -> dict:
    params = dict(serial_number=profile_number)
    url = "http://local.adspower.net:50325/api/v1/browser/start"
    response = requests.get(url, params=params)
    data = response.json()
    return data


def main():
    profile_data = open_browser(941)
    url_connect = profile_data.get('data').get('ws').get('puppeteer')
    pw = sync_playwright().start()
    browser = pw.chromium.connect_over_cdp(url_connect)
    if not browser.is_connected():
        print("Browser not connected")
        exit(1)
    context = browser.contexts[0]
    page = context.pages[0]

    """Настройка таймаутов"""
    # установка таймаута для всех методов внутри page
    page.set_default_timeout(30000)
    # установка таймаута для методов навигации внутри page
    page.set_default_navigation_timeout(30000)

    # проверка закрыта ли страница, если да возвращает True
    page.is_closed()

    print(page.url)  # возвращает текущий URL страницы
    print(page.title())  # возвращает заголовок страницы

    # поиск вкладки по URL и закрытие
    for page in context.pages:
        if 'google' in page.url:
            page.close()
            break

    # сделать вкладку активной
    page.bring_to_front()

    # переход на страницу
    page.goto('google.com', wait_until='load', referer='https://ya.ru')

    # ожидание загрузки страницы
    page.wait_for_load_state('load')

    # возврат на предыдущую страницу
    page.go_back()
    # возврат на следующую страницу
    page.go_forward()

    page.reload()  # перезагрузка страницы

    page.close()  # закрытие страницы

    # ожидание загрузки страницы по URL
    page.wait_for_url('https://www.google.com/')

    # добавление заголовка к запросу
    page.set_extra_http_headers({'key': 'value-key'})

    current_ip = page.evaluate('''
               async () => {
                   const response = await fetch('https://api.ipify.org');
                   const data = await response.text();
                   return data;
               }
           ''')

    # ловец открывающихся страниц
    with context.expect_page() as page_catcher:
        page.get_by_title('EventEmitter').click()
    new_page = page_catcher.value

    # ловец открывающихся страниц
    with page.expect_popup() as page_catcher:
        page.get_by_title('EventEmitter').click()
    new_page = page_catcher.value

    # codegen
    page.pause()



if __name__ == '__main__':
    main()

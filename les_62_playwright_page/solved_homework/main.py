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

    # переходим по url с ожиданием прогрузки страницы
    page.goto('https://pancakeswap.finance/', wait_until='load')
    # кликаем на кнопку Connect Wallet
    page.locator('//div[text()="Connect Wallet"]').first.click()
    # запускаем контекст ожидания страницы
    with context.expect_page() as page_catcher:
        # кликаем на кнопку Metamask
        page.locator('//img[contains(@src, "metamask")]').first.click()
    # извлекаем страницу из контекста ожидания
    metamask_page = page_catcher.value
    # ожидаем загрузки страницы
    metamask_page.wait_for_load_state('load')
    # кликаем на кнопку Next в Metamask
    metamask_page.locator('//button[@data-testid="page-container-footer-next"]').first.click()
    # ожидаем загрузки страницы
    metamask_page.wait_for_load_state('load')
    # кликаем на кнопку Next в Metamask
    metamask_page.locator('//button[@data-testid="page-container-footer-next"]').first.click()



if __name__ == '__main__':
    main()

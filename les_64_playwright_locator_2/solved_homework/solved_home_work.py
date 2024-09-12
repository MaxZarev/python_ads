""""""
import random

"""
Написать скрипт, который будет открывать страницу
uniswap.org
Подключать кошелек к сайту
Выбирать первый токен для обмена USDT
Второй токен для обмена ETH
Вводить рандомную сумму обмена в токенах USDT от 1.50 до 2.50
В поле ввода вводите сумму с помощью метода fill у объекта Locator.
И производить операцию обмена токенов с подписанием транзакции в метамаске.

Нужную сеть можете указать заранее в метамаске, например Arbitrum.
"""

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
    profile_data = open_browser(949)
    url_connect = profile_data.get('data').get('ws').get('puppeteer')
    pw = sync_playwright().start()
    browser = pw.chromium.connect_over_cdp(url_connect, slow_mo=1000)
    if not browser.is_connected():
        print("Browser not connected")
        exit(1)
    context = browser.contexts[0]
    page = context.pages[0]

    # переходим по url
    page.goto('https://app.uniswap.org/swap?chain=arbitrum', wait_until='load')

    # подключение кошелька, если он не подключен
    connect_button = page.get_by_test_id('navbar-connect-wallet')
    if connect_button.count() > 0:
        connect_button.click()
        with context.expect_page() as page_catcher:
            page.get_by_role('button', name='MetaMask').click()
        metamask_page = page_catcher.value
        metamask_page.wait_for_load_state('load')
        metamask_page.get_by_test_id('page-container-footer-next').click()
        metamask_page.get_by_test_id('page-container-footer-next').click()

    # выбор токенов для обмена
    page.locator('button.open-currency-select-button').first.click()
    page.get_by_test_id('chain-selector').click()
    page.get_by_text('Arbitrum', exact=True).click()
    page.get_by_test_id('explore-search-input').fill('USDT')
    page.get_by_text('Search results').wait_for(state='visible')
    page.locator('//div[contains(@data-testid, "token-option")]').filter(has_text='Arbitrum').filter(has_text='USDT').click()

    page.get_by_test_id('currency-undefined-undefined').click()
    time.sleep(3)
    page.get_by_test_id('explore-search-input').fill('ETH')
    page.get_by_text('Search results').wait_for(state='visible')
    page.get_by_text('Arbitrum ETH').click()

    amount = 7 #round(random.uniform(1.50, 2.50))
    page.get_by_placeholder('0').first.fill(str(amount))
    time.sleep(5)
    page.get_by_test_id('swap-button').click()
    page.get_by_text('Review swap').wait_for(state='visible')
    swap_text = page.get_by_test_id('confirm-swap-button').inner_text()
    with context.expect_page(timeout=150*1000) as page_catcher:
        page.get_by_test_id('confirm-swap-button').click()
    metamask_page = page_catcher.value

    if swap_text == 'Approve and swap':
        metamask_page.wait_for_load_state('load')
        apr_amount = amount * 1.5
        metamask_page.get_by_test_id('custom-spending-cap-input').fill(str(apr_amount))
        metamask_page.get_by_test_id('page-container-footer-next').click()
        metamask_page.get_by_test_id('page-container-footer-next').click()

        with context.expect_page(timeout=150*1000) as page_catcher:
            time.sleep(5)
        metamask_page = page_catcher.value
        metamask_page.wait_for_load_state('load')
        if metamask_page.get_by_test_id('signature-request-scroll-button').count() > 0:
            metamask_page.get_by_test_id('signature-request-scroll-button').click()
            metamask_page.get_by_test_id('page-container-footer-next').click()

            with context.expect_page(timeout=150*1000) as page_catcher:
                time.sleep(5)
            metamask_page = page_catcher.value

    metamask_page.wait_for_load_state('load')
    metamask_page.get_by_test_id('page-container-footer-next').click()

    for _ in range(100):
        if page.get_by_test_id('confirmed-icon').count() > 0:
            break
        time.sleep(5)




    pass



if __name__ == '__main__':
    main()

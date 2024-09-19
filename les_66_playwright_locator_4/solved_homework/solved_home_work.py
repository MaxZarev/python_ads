""""""


"""
Прочитайте за что отвечает параметр slow_mo в методе connect_over_cdp 
https://playwright.dev/python/docs/next/api/class-browsertype#browser-type-connect-over-cdp

Будьте осторожны с вкладкой у которой в url offscreen, данную вкладку нельзя закрывать и нельзя
использовать для перехода по ссылкам, это техническая вкладка, игнорируйте ее.

Написать скрипт, который:
1. Запускает профиль со задержкой действий slow_mo 1 секунда
2. Закрывает все вкладки, кроме одной (*попытка закрыть вкладку с url offscreen вызовет ошибку)
3. Открывает метамаск, вводит пароль, авторизуется и выбирает сеть Linea
4. Переход на https://linea.build/
5. Внутри Ecosystem выбирает Applications
6. Внутри All apps выбирает фильтр Defi, чтобы на страницу отфильтровало приложения
    и оставило только Defi
7. Прокручивает страницу пока не найдет до SushiSwap
8. Нажимает по ссылку SushiSwap 
9. Делает открывшуюся страницу активной
10. Подключает кошелек (учитываем ситуацию, если кошелек был подключен ранее)
11. Нажимает на кнопку выбора второго токена
12. Берет и перемешивает список из названий токенов 'usdc', 'cake', 'ust', 'manta', 'btc', 'usdt'
14. В поле поиска необходимо ввести название токена посимвольно с паузой в долю секунды,
    после ввода нужно проверить есть ли среди найденных токенов, токен 'USDT',
    если есть выбираем его, если нет вводим следующий токен из списка.
15. После выбора токена вводит в первое поле рандомную сумму не более 0.0002
16. Проверяет сколько можно получить USDT, если меньше 3$, увеличивает изначальную сумму на 50%
    и вводит повторно, делает так пока сумма получаемых токенов не будет больше 3$
17. Нажимает Swap
18. В открывшемся окне подтверждает свап.
19. В метамаске устанавливает газ Aggressive.
20. В метамаске кнопка подтверждения транзакции имеет способность становится неактивной, давайте 
    поймаем ее состояние disabled и попробуем в этот момент запустить клик по ней, чтобы понять
    как работает клик с такими кнопками, будет ли он ждать или вызовет ошибку.
    Скрипт должен в цикле ловить состояние кнопки disabled, сразу как поймает
    должен напечатать  в терминале: "сейчас кнопка disabled, давай попробуем нажать"
    и запускает клик по ней.
21. Достает во всплывающем окне hash транзакции.
22. Подключается к rpc ноде Linea через библиотеку WEB и при помощи метода Web3.eth.wait_for_transaction_receipt(hash_tx)
    получает чек об транзакции и смотрит там статус
23. Если статус 1, пишем уведомление об успешности транзакции обмена, адрес кошелька с
    которого сделана транзакция и хеш (берет данные в чеке)

"""

import time
import random
import requests
from playwright.sync_api import sync_playwright
from web3 import Web3


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

    time.sleep(5)

    for page_close in context.pages:
        if page != page_close and 'offscreen' not in page_close.url:
            page_close.close()

    page.goto('chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html', wait_until='load')

    # переходим по url

    if page.get_by_test_id('unlock-password').count():
        password = '12345678'
        page.get_by_test_id('unlock-password').fill(password)
        page.get_by_test_id('unlock-submit').click()

    page.wait_for_load_state(state='load')
    network_button = page.get_by_test_id('network-display')
    if 'linea' not in network_button.inner_text().lower():
        network_button.click()
        page.locator('section').get_by_text('Linea').click()

    page.goto('https://linea.build', wait_until='load')

    # наводим курсор на Ecosystem
    page.get_by_role('listitem').filter(has_text='Ecosystem').hover()

    page.get_by_role('link', name='Applications').click()

    page.get_by_role('button', name='All apps').hover()

    page.locator('label').get_by_text('Defi').click()


    sushi_button = page.get_by_role('link', name='Sushi')
    while not sushi_button.count():
        page.locator('footer').scroll_into_view_if_needed()

    with context.expect_page() as page_catcher:
        sushi_button.click()

    sushi_page = page_catcher.value
    sushi_page.bring_to_front()

    connect_button = sushi_page.get_by_role('button', name='Connect Wallet').first
    if connect_button.count():
        connect_button.click()
        with context.expect_page() as page_catcher:
            sushi_page.get_by_text('MetaMask').click()
        metamask_page = page_catcher.value
        metamask_page.get_by_test_id('page-container-footer-next').click()
        metamask_page.get_by_test_id('page-container-footer-next').click()

    sushi_page.locator('button[testdata-id=swap-to-button]').click()

    tokens = ['usdc', 'cake', 'ust', 'manta', 'btc', 'usdt']
    random.shuffle(tokens)

    search = sushi_page.get_by_placeholder('Search by token or address')
    for token in tokens:
        for symbol in token:
            search.press(symbol)
            pause = random.uniform(0.0005, 0.0025)
            time.sleep(pause)

        if not sushi_page.get_by_text('No tokens found.').count():
            if sushi_page.get_by_text('USDT', exact=True).count():
                break
        search.clear()

    sushi_page.get_by_text('USDT', exact=True).click()

    input_textbox = sushi_page.get_by_placeholder('0.0').first
    output_textbox = sushi_page.get_by_placeholder('0.0').last

    amount = random.uniform(0.0001, 0.0002)

    while True:
        amount = round(amount, 5)
        for num in str(amount):
            input_textbox.press(num)

        usdt_amount = output_textbox.input_value()
        if float(usdt_amount) > 3:
            break

        amount *= 1.5
        input_textbox.clear()

    sushi_page.locator('button[testdata-id=swap-button]').click()

    with context.expect_page() as page_catcher:
        sushi_page.locator('button[testdata-id=confirm-swap-button]').click()
    metamask_page = page_catcher.value
    metamask_page.get_by_test_id('edit-gas-fee-icon').click()
    metamask_page.get_by_test_id('edit-gas-fee-item-high').click()
    confirm_button = metamask_page.get_by_test_id('page-container-footer-next')
    while True:
        if confirm_button.is_disabled():
            print('сейчас кнопка disabled, давай попробуем нажать')
            confirm_button.click()
            break

    sushi_page.get_by_text('Success!').wait_for(state='visible', timeout=10000)
    link = sushi_page.get_by_role('link', name='You sold').get_attribute('href')
    hash_tx = link.split('/')[-1]

    w3 = Web3(Web3.HTTPProvider('https://1rpc.io/linea'))
    receipt = w3.eth.wait_for_transaction_receipt(hash_tx)
    if receipt.get('status'):
        print(f'Успешный свап на кошельке {receipt.get("from")} hash: {hash_tx} ')

    pass






if __name__ == '__main__':
    main()

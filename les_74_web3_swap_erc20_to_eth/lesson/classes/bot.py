import random
import time

from classes.ads import Ads
from classes.excel import Excel
from classes.metamask import Metamask
from classes.okx_py import OKX
from classes.onchain import Onchain
from config import chain

class Bot:
    def __init__(self, profile_number: int, private_key: str) -> None:
        self.ads = Ads(profile_number)
        self.metamask = Metamask(self.ads)
        self.okx = OKX()
        self.excel = Excel()
        self.onchain = Onchain(private_key)

    def run_activity(self):

        self.metamask.auth_metamask()
        self.metamask.select_chain(chain)
        self.ads.page.goto('https://linea.build', wait_until='load')

        # наводим курсор на Ecosystem
        self.ads.page.get_by_role('listitem').filter(has_text='Ecosystem').hover()

        self.ads.page.get_by_role('link', name='Applications').click()

        self.ads.page.get_by_role('button', name='All apps').hover()

        self.ads.page.locator('label').get_by_text('Defi').click()

        sushi_button = self.ads.page.get_by_role('link', name='Sushi')
        while not sushi_button.count():
            self.ads.page.locator('footer').scroll_into_view_if_needed()

        with self.ads.context.expect_page() as page_catcher:
            sushi_button.click()

        sushi_page = page_catcher.value
        sushi_page.bring_to_front()

        connect_button = sushi_page.get_by_role('button', name='Connect Wallet').first
        if connect_button.count():
            connect_button.click()
            with self.ads.context.expect_page() as page_catcher:
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

        balance = self.onchain.get_balance()
        if amount > balance.ether_float:
            print('недостаточно средств на кошельке')
            self.okx.withdraw(self.onchain.address, 'ERC20', 'ETH', amount)

        sushi_page.locator('button[testdata-id=swap-button]').click()

        with self.ads.context.expect_page() as page_catcher:
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


        receipt = self.onchain.w3.eth.wait_for_transaction_receipt(hash_tx)
        if receipt.get('status'):
            print(f'Успешный свап на кошельке {receipt.get("from")} hash: {hash_tx} ')



    def close(self):
        self.ads.close_browser()


from playwright.sync_api import Locator

from classes.ads import Ads
from config import metamask_url
from utils import random_sleep, generate_password, write_text_to_file


class Metamask:
    chains = {
        "Linea ANKR": {
            "Network name": "Linea ANKR",
            "New RPC URL": "https://rpc.ankr.com/linea",
            "Chain ID": 59144,
            "Currency Symbol": "ETH",
        },
        "BSC": {
            "Network name": "BSC",
            "New RPC URL": "https://bsc-pokt.nodies.app",
            "Chain ID": 56,
            "Currency Symbol": "BNB",
        },

    }

    def __init__(self, ads: Ads, password: str = None, seed: str = None):
        self._url = metamask_url
        self.ads = ads
        self.password = password
        self.seed = seed

    def open_metamask(self):
        """
        Открывает metamask
        :return:
        """
        self.ads.open_url(self._url)

    def create_wallet(self):
        """
        Создает кошелек в metamask
        :return:
        """
        self.open_metamask()
        self.ads.page.get_by_test_id('onboarding-terms-checkbox').click()
        self.ads.page.get_by_test_id('onboarding-create-wallet').click()
        self.ads.page.get_by_test_id('metametrics-no-thanks').click()

        # генерируем пароль и вводим в 2 поля
        if not self.password:
            self.password = generate_password()
        self.ads.page.get_by_test_id('create-password-new').fill(self.password)
        self.ads.page.get_by_test_id('create-password-confirm').fill(self.password)
        self.ads.page.get_by_test_id('create-password-terms').click()
        self.ads.page.get_by_test_id('create-password-wallet').click()

        self.ads.page.get_by_test_id('secure-wallet-recommended').click()
        self.ads.page.get_by_test_id('recovery-phrase-reveal').click()

        seed = []
        for i in range(12):
            test_id = f"recovery-phrase-chip-{i}"
            word = self.ads.page.get_by_test_id(test_id).inner_text()
            seed.append(word)

        self.ads.page.get_by_test_id('recovery-phrase-next').click()
        for i in range(12):
            if self.ads.page.get_by_test_id(f'recovery-phrase-input-{i}').count():
                self.ads.page.get_by_test_id(f'recovery-phrase-input-{i}').fill(seed[i])
        self.ads.page.get_by_test_id('recovery-phrase-confirm').click()
        random_sleep(3, 5)
        self.ads.page.get_by_test_id('onboarding-complete-done').click()
        self.ads.page.get_by_test_id('pin-extension-next').click()
        self.ads.click_if_exists(method='test_id', value='pin-extension-done')
        random_sleep(3, 3)
        self.ads.click_if_exists(method='test_id', value='popover-close')

        address = self.get_address()

        seed_str = " ".join(seed)

        write_text_to_file("new_wallets.txt", f"{self.ads.profile_number} {address} {self.password} {seed_str}")

    def auth_metamask(self) -> None:
        """
        Авторизует в metamask
        :return:
        """
        self.open_metamask()
        if self.ads.page.get_by_test_id('unlock-password').count():
            self.ads.page.get_by_test_id('unlock-password').fill(self.password)
            self.ads.page.get_by_test_id('unlock-submit').click()
            random_sleep(3, 5)

            self.ads.click_if_exists(method='test_id', value='popover-close')

        if self.ads.page.get_by_test_id('account-options-menu-button').count():
            print(f"{self.ads.profile_number} успешно авторизован в metamask")
        else:
            print(f"{self.ads.profile_number} ошибка авторизации в metamask")

    def import_wallet(self):
        """
        Импортирует кошелек в metamask
        :return:
        """
        self.open_metamask()

        seed_list = self.seed.split(" ")
        if not self.password:
            self.password = generate_password()

        if self.ads.page.get_by_test_id('onboarding-create-wallet').count():
            self.ads.page.get_by_test_id('onboarding-terms-checkbox').click()
            self.ads.page.get_by_test_id('onboarding-import-wallet').click()
            self.ads.page.get_by_test_id('metametrics-no-thanks').click()
            for i, word in enumerate(seed_list):
                self.ads.page.get_by_test_id(f"import-srp__srp-word-{i}").fill(word)
            self.ads.page.get_by_test_id('import-srp-confirm').click()
            self.ads.page.get_by_test_id('create-password-new').fill(self.password)
            self.ads.page.get_by_test_id('create-password-confirm').fill(self.password)
            self.ads.page.get_by_test_id('create-password-terms').click()
            self.ads.page.get_by_test_id('create-password-import').click()
            random_sleep(3, 5)
            self.ads.page.get_by_test_id('onboarding-complete-done').click()
            self.ads.page.get_by_test_id('pin-extension-next').click()
            self.ads.click_if_exists(method='test_id', value='pin-extension-done')

        else:
            self.ads.page.get_by_text('Forgot password?').click()
            for i, word in enumerate(seed_list):
                self.ads.page.get_by_test_id(f"import-srp__srp-word-{i}").fill(word)
            self.ads.page.get_by_test_id('create-vault-password').fill(self.password)
            self.ads.page.get_by_test_id('create-vault-confirm-password').fill(self.password)
            self.ads.page.get_by_test_id('create-new-vault-submit-button').click()

        random_sleep(3, 3)
        self.ads.click_if_exists(method='test_id', value='popover-close')
        address = self.get_address()
        seed_str = " ".join(seed_list)
        write_text_to_file("new_wallets.txt",
                           f"{self.ads.profile_number} {address} {self.password} {seed_str}")



    def get_address(self) -> str:
        """
        Возвращает адрес кошелька
        :return: адрес кошелька
        """
        self.ads.page.get_by_test_id('account-options-menu-button').click()
        self.ads.page.get_by_test_id('account-list-menu-details').click()
        address = self.ads.page.get_by_test_id('address-copy-button-text').inner_text()
        self.ads.page.get_by_role('button', name='Close').first.click()
        return address

    def connect(self, locator: Locator, timeout: int = 30) -> None:
        """
        Подтверждает подключение к metamask
        :return:
        """

        try:
            with self.ads.context.expect_page(timeout=timeout) as page_catcher:
                locator.click()
            metamask_page = page_catcher.value
        except:
            metamask_page = self.ads.catch_page(['connect', 'confirm-transaction'])
            if not metamask_page:
                raise Exception(f"Error: {self.ads.profile_number} Ошибка подключения метамаска")

        metamask_page.wait_for_load_state('load')

        confirm_button = metamask_page.get_by_test_id('page-container-footer-next')
        if not confirm_button.count():
            confirm_button = metamask_page.get_by_test_id('confirm-footer-button')

        confirm_button.click()
        random_sleep(1, 3)
        if not metamask_page.is_closed():
            confirm_button.click()

    def sign(self, locator: Locator, timeout: int = 30) -> None:
        """
        Подтверждает подпись в metamask
        :return:
        """
        try:
            with self.ads.context.expect_page(timeout=timeout) as page_catcher:
                locator.click()
            metamask_page = page_catcher.value
        except:
            metamask_page = self.ads.catch_page(['confirm-transaction'])
            if not metamask_page:
                raise Exception(f"Error: {self.ads.profile_number} Ошибка подписи сообщения в метамаске)")

        metamask_page.wait_for_load_state('load')

        confirm_button = metamask_page.get_by_test_id('page-container-footer-next')
        if not confirm_button.count():
            confirm_button = metamask_page.get_by_test_id('confirm-footer-button')

        confirm_button.click()

    def send_tx(self, locator: Locator, timeout: int = 30) -> None:
        """
        Подтверждает отправку транзакции в metamask
        :return:
        """
        try:
            with self.ads.context.expect_page(timeout=timeout) as page_catcher:
                locator.click()
            metamask_page = page_catcher.value
        except:
            metamask_page = self.ads.catch_page(['confirm-transaction'])
            if not metamask_page:
                raise Exception(f"Error: {self.ads.profile_number} Ошибка подтверждения транзакции метамаска")

        metamask_page.wait_for_load_state('load')

        confirm_button = metamask_page.get_by_test_id('page-container-footer-next')
        if not confirm_button.count():
            confirm_button = metamask_page.get_by_test_id('confirm-footer-button')

        confirm_button.click()

    def select_chain(self, chain: str):
        """
        Выбирает сеть в metamask
        :param chain: название сети как в метамаске
        :return:
        """
        chain_button = self.ads.page.get_by_test_id("network-display")
        if chain in chain_button.inner_text():
            return
        chain_button.click()
        random_sleep(1, 3)

        if self.ads.page.get_by_text(chain).count():
            self.ads.page.get_by_text(chain).click()
        else:
            self.ads.page.get_by_role('button', name='Close').first.click()
            self.set_chain(chain)


    def set_chain(self, chain: str):
        """
        Добавляет новую сеть в metamask
        :param chain: название сети
        :return:
        """

        chain_name = self.chains[chain]["Network name"]
        rpc = self.chains[chain]["New RPC URL"]
        chain_id = str(self.chains[chain]["Chain ID"])
        currency = self.chains[chain]["Currency Symbol"]
        self.ads.open_url(self._url + "#settings/networks/add-network")
        random_sleep(1, 3)
        self.ads.page.get_by_test_id('network-form-network-name').fill(chain_name)
        self.ads.page.get_by_test_id('network-form-rpc-url').fill(rpc)
        self.ads.page.get_by_test_id('network-form-chain-id').fill(chain_id)
        self.ads.page.get_by_test_id('network-form-ticker-input').fill(currency)
        random_sleep(1, 3)
        self.ads.page.get_by_role('button', name='Save').or_(self.ads.page.get_by_role('button', name='Сохранить')).click()
        self.ads.page.get_by_role('heading', name='Switch to').or_(self.ads.page.get_by_role('button', name='Сменить на')).click()

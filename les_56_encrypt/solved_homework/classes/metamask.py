from classes.ads import Ads
from utils import sleep_random, generate_password, salt_password, shuffle_password, shuffle_seed, unshuffle_seed, encrypt_data, decrypt_data


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

    def open_metamask(self):
        """
        Открывает metamask
        :return: None
        """
        self.ads.open_url(self._url)

    def create_wallet(self):
        """
        Создает кошелек в metamask, сохраняет результат в excel
        :return: None
        """
        self.open_metamask()
        sleep_random()
        self.ads.click_element("//input[@data-testid='onboarding-terms-checkbox']")
        sleep_random()
        self.ads.click_element("//button[@data-testid='onboarding-create-wallet']")
        sleep_random()
        self.ads.click_element("//button[@data-testid='metametrics-no-thanks']")

        # генерируем пароль и вводим в 2 поля
        self.password = generate_password()

        self.ads.input_text("//input[@data-testid='create-password-new']", self.password)
        sleep_random()
        self.ads.input_text("//input[@data-testid='create-password-confirm']", self.password)
        sleep_random()
        self.ads.click_element("//input[@data-testid='create-password-terms']")
        sleep_random()
        self.ads.click_element("//button[@data-testid='create-password-wallet']")
        sleep_random()
        self.ads.click_element("//button[@data-testid='secure-wallet-recommended']")
        sleep_random()
        self.ads.click_element("//button[@data-testid='recovery-phrase-reveal']")
        seed = []
        for i in range(12):
            xpath = f"//div[@data-testid='recovery-phrase-chip-{i}']"
            word = self.ads.get_text(xpath)
            seed.append(word)
        sleep_random()
        self.ads.click_element("//button[@data-testid='recovery-phrase-next']")
        sleep_random()
        for i in range(12):
            self.ads.input_text(f"//input[@data-testid='recovery-phrase-input-{i}']", seed[i], timeout=1)
            sleep_random()
        sleep_random()
        self.ads.click_element("//button[@data-testid='recovery-phrase-confirm']")
        sleep_random(3, 5)
        self.ads.click_element("//button[@data-testid='onboarding-complete-done']")

        sleep_random()
        self.ads.click_element("//button[@data-testid='pin-extension-next']")
        sleep_random()
        self.ads.click_element("//button[@data-testid='pin-extension-done']")
        sleep_random(3, 3)
        self.ads.click_element("//button[@data-testid='popover-close']", 5)
        sleep_random()

        self.ads.click_element("//button[@data-testid='account-options-menu-button']")
        sleep_random()

        self.ads.click_element("//button[@data-testid='account-list-menu-details']")
        sleep_random()

        address = self.ads.get_text("//button[@data-testid='address-copy-button-text']/span/div")
        sleep_random()

        encrypt_seed = encrypt_data(" ".join(seed))
        encrypt_password = encrypt_data(self.password)

        self.ads.excel.add_row([address, encrypt_password, self.ads.profile_number, encrypt_seed])

    def auth_metamask(self) -> None:
        """
        Проверяет есть ли авторизация, если нет, то авторизует
        :return:
        """
        self.open_metamask()
        # проверяем есть ли уже авторизация в кошельке, если да выходим из метода
        if self.ads.find_element("//li[@data-testid='home__nfts-tab']", 3):
            return
        # расшифровываем пароль и вводим
        self.ads.input_text("//input[@data-testid='unlock-password']", decrypt_data(self.password))
        self.ads.click_element("//button[@data-testid='unlock-submit']")
        sleep_random(3, 5)
        self.ads.click_element("//button[@data-testid='popover-close']", 5)
        # проверяем успешность авторизации
        if not self.ads.find_element("//li[@data-testid='home__nfts-tab']", 3):
            raise Exception("Metamask auth failed")

    def import_wallet(self):
        """
        Импортирует кошелек в metamask, сохраняет результат в excel
        :return: None
        """
        self.open_metamask()

        seed_list = decrypt_data(self.seed).split(" ")
        if not self.password:
            self.password = generate_password()

        if self.ads.find_element("//button[@data-testid='onboarding-create-wallet']", 5):
            self.ads.click_element("//input[@data-testid='onboarding-terms-checkbox']")
            sleep_random()
            self.ads.click_element("//button[@data-testid='onboarding-import-wallet']")
            self.ads.click_element("//button[@data-testid='metametrics-no-thanks']")
            for i, word in enumerate(seed_list):
                self.ads.input_text(f"//input[@data-testid='import-srp__srp-word-{i}']", word)

            self.ads.click_element("//button[@data-testid='import-srp-confirm']")

            self.ads.input_text("//input[@data-testid='create-password-new']", self.password)
            self.ads.input_text("//input[@data-testid='create-password-confirm']", self.password)
            sleep_random()
            self.ads.click_element("//input[@data-testid='create-password-terms']")
            self.ads.click_element("//button[@data-testid='create-password-import']")

            sleep_random(3, 5)
            self.ads.click_element("//button[@data-testid='onboarding-complete-done']")

            sleep_random()
            self.ads.click_element("//button[@data-testid='pin-extension-next']")
            sleep_random()
            self.ads.click_element("//button[@data-testid='pin-extension-done']")
            sleep_random(3, 3)
            self.ads.click_element("//button[@data-testid='popover-close']", 5)
            sleep_random()
        else:
            self.ads.click_element("//a[text()='Forgot password?']", 5)
            for i, word in enumerate(seed_list):
                self.ads.input_text(f"//input[@data-testid='import-srp__srp-word-{i}']", word)
            self.ads.input_text("//input[@data-testid='create-vault-password']", self.password)
            self.ads.input_text("//input[@data-testid='create-vault-confirm-password']", self.password)
            self.ads.click_element("//button[@data-testid='create-new-vault-submit-button']")
            sleep_random(3, 3)
            self.ads.click_element("//button[@data-testid='popover-close']", 5)

        self.ads.click_element("//button[@data-testid='account-options-menu-button']")
        sleep_random()

        self.ads.click_element("//button[@data-testid='account-list-menu-details']")
        sleep_random()

        address = self.ads.get_text("//button[@data-testid='address-copy-button-text']/span/div")
        encrypt_password = encrypt_data(self.password)

        self.ads.excel.add_row([address, encrypt_password, self.ads.profile_number, self.seed])


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

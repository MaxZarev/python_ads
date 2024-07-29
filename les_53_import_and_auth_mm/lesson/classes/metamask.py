from classes.ads import Ads
from utils import sleep_random, generate_password
from utils import write_text_to_file


class Metamask:

    def __init__(self, ads, password: str = None, seed: str = None):
        self._url = "chrome-extension://kfffndnaofmhjgfjincifaloeplkongj/home.html#"
        self.ads: Ads = ads
        self.password = password
        self.seed = seed

    def open_metamask(self):
        self.ads.open_url(self._url)

    def create_wallet(self):
        self.open_metamask()
        sleep_random()
        self.ads.click_element("//input[@data-testid='onboarding-terms-checkbox']")
        sleep_random()
        self.ads.click_element("//button[@data-testid='onboarding-create-wallet']")
        sleep_random()
        self.ads.click_element("//button[@data-testid='metametrics-no-thanks']")

        # генерируем пароль и вводим в 2 поля
        password = generate_password()
        self.ads.input_text("//input[@data-testid='create-password-new']", password)
        sleep_random()
        self.ads.input_text("//input[@data-testid='create-password-confirm']", password)
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

        seed_str = " ".join(seed)

        write_text_to_file("wallets.txt", f"{address} {password} {seed_str}")

    def auth_metamask(self) -> None:
        self.open_metamask()
        self.ads.input_text("//input[@data-testid='unlock-password']", self.password)
        self.ads.click_element("//button[@data-testid='unlock-submit']")
        sleep_random(3, 5)
        self.ads.click_element("//button[@data-testid='popover-close']", 5)
        if not self.ads.find_element("//button[@data-testid='home__nfts-tab']", 5):
            raise Exception("Metamask auth failed")

    def import_wallet(self):
        self.open_metamask()

        seed_list = self.seed.split(" ")
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
        sleep_random()

        write_text_to_file("wallets.txt", f"{address} {self.password} {self.seed}")
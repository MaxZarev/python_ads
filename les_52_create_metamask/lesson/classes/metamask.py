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

    def auth_metamask(self):
        pass

    def import_wallet(self):
        pass



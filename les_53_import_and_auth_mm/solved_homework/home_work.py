""""""

""" 
Реализовать метод у класса Metamask:

def import_wallet(self):
    pass

def auth_metamask(self):
    pass
    
Метод import_wallet должен импортировать кошелек в MetaMask по сид фразе.
Метод auth_metamask должен авторизовать пользователя в MetaMask.

"""


def auth_metamask(self) -> bool:
    """
    Авторизация в метамаске
    :return: True если авторизация прошла успешно
    """
    # Открываем метамаск
    self.open_metamask()

    # Проверяем, если открытая страница имеет элементы авторизованного кошелька, возвращаем True
    xpath_open_wallet = "//button[@data-testid='import-token-button']"
    if self.ads.find_element(xpath_open_wallet, 5):
        return True

    # Вводим пароль
    self.ads.input_text("//input[@data-testid='unlock-password']", self.password)
    self.ads.click_element("//button[@data-testid='unlock-submit']")
    sleep_random()
    # Проверяем, если открытая страница имеет элементы авторизованного кошелька, возвращаем True, иначе False
    if self.ads.find_element(xpath_open_wallet):
        return True
    else:
        return False


def import_wallet(self):
    """
    Импорт кошелька в метамаск из seed фразы и генерация пароля
    :return: None
    """
    # Открываем метамаск
    self.open_metamask()

    sleep_random()
    self.ads.click_element("//input[@data-testid='onboarding-terms-checkbox']")
    sleep_random()
    self.ads.click_element("//button[@data-testid='onboarding-import-wallet']")
    sleep_random()
    self.ads.click_element("//button[@data-testid='metametrics-no-thanks']")
    sleep_random()
    seed_list = self.seed.split(" ")
    for i, word in enumerate(seed_list):
        self.ads.input_text(f"//input[@data-testid='import-srp__srp-word-{i}']", word)

    self.ads.click_element("//button[@data-testid='import-srp-confirm']")

    password = generate_password()
    self.ads.input_text("//input[@data-testid='create-password-new']", password)
    self.ads.input_text("//input[@data-testid='create-password-confirm']", password)
    sleep_random()
    self.ads.click_element("//input[@data-testid='create-password-terms']")
    sleep_random()
    self.ads.click_element("//button[@data-testid='create-password-import']")
    sleep_random()
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

    write_text_to_file("wallets.txt", f"{address} {password} {self.seed}")

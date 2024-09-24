from classes.ads import Ads
from classes.excel import Excel
from classes.metamask import Metamask
from classes.okx_py import OKX
from classes.onchain import Onchain


class Bot:
    def __init__(self, profile_number: int, private_key: str) -> None:
        self.ads = Ads(profile_number)
        self.metamask = Metamask(self.ads)
        self.okx = OKX()
        self.excel = Excel()
        self.onchain = Onchain(private_key)

    def activity(self):

        self.metamask.auth_metamask()
        self.ads.open_url("https://www.okx.com/")
        self.swap()

        self.pancake.swap()


    def swap(self):
        # описание активаности свапа
        pass

    def withdraw(self):
        pass

    def close(self):
        self.ads.close_browser()


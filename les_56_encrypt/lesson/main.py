
from classes.ads import Ads
from classes.metamask import Metamask

from utils import sleep_random

def main():
    ads = Ads(949, "185.149.21.78:3000:jINV9g:DXqi8PtrAp")
    metamask = Metamask(ads, password="'5Uj>AK^Sfb`$,MCzfOJ2{mO:;", seed="super impose give glimpse food initial artist figure loop jazz today cruel")
    metamask.auth_metamask()
    metamask.select_network("Binance Smart Chain")
    sleep_random(5, 10)
    ads.close_browser()




if __name__ == '__main__':
    main()

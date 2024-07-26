
from classes.ads import Ads
from classes.metamask import Metamask

from utils import sleep_random

def main():
    ads = Ads(940, "185.149.21.78:3000:jINV9g:DXqi8PtrAp")
    metamask = Metamask(ads, "123456")
    metamask.import_wallet()
    sleep_random(5, 10)
    ads.close_browser()







if __name__ == '__main__':
    main()

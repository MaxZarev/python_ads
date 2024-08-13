
from classes.ads import Ads
from classes.metamask import Metamask

from utils import sleep_random, get_list_from_file


def main():
    profiles = [int(profile) for profile  in get_list_from_file("profiles.txt")]
    for profile in profiles:
        ads = Ads(profile)
        ads.OKX.withdrawal()
        metamask = Metamask(ads)
        metamask.create_wallet()
        sleep_random(3, 7)
        ads.close_browser()

    for profile in profiles:
        ads = Ads(profile)
        password = ads.excel.get_cell(profile, "Password")
        metamask = Metamask(ads, password=password)
        metamask.auth_metamask()
        sleep_random(3, 7)
        ads.close_browser()

    print("Создано 10 кошельков и авторизовано в них.")




if __name__ == '__main__':
    main()

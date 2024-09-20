
from classes.ads import Ads

from utils import random_sleep, get_list_from_file


def main():
    ads = Ads(949)
    ads.open_url("google.com")

    # автоматизация
    random_sleep(10)
    ads.close_browser()

if __name__ == '__main__':
    main()

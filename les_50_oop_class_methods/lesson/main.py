
from ads import Ads
from utils import sleep_random

def main():
    try:
        ads = Ads(749, "185.149.21.78:3000:jINV9g:DXqi8PtrAp")
        ads.open_url("google.com")
        ads.open_url("google.com")
        sleep_random(5, 10)
        ads.close_browser()
        text = ads.get_text("//span")
    except Exception as ex:
        print(ex)



if __name__ == '__main__':
    main()

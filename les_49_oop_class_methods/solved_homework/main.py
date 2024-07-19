from les_49_oop_class_methods.solved_homework.classes import Ads


def main():
    ads = Ads(949, "185.149.21.78:3000:jINV9g:DXqi8PtrAp")
    ads.driver.get("https://google.com")
    ads.sleep_random(10, 20)

if __name__ == '__main__':
    main()
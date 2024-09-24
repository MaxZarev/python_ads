
from classes.bot import Bot
from utils import get_list_from_file

def main():
    profiles =  get_list_from_file("profiles.txt")
    private_keys = get_list_from_file("private_keys.txt")


    for profile_number, private_key in zip(profiles, private_keys):

        bot = Bot(profile_number, private_key)
        try:
            bot.activity()
        except Exception as e:
            print(f"Ошибка в профиле {profile_number}, {e}")
        finally:
            bot.close()







if __name__ == '__main__':
    main()

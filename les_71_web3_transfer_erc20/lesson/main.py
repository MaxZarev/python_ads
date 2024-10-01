
from classes.bot import Bot
from utils import get_list_from_file

def main():
    profiles =  get_list_from_file("profiles.txt.txt")
    private_keys = get_list_from_file("private_keys.txt")

    for profile_number, private_key in zip(profiles, private_keys):
        print(f"Запуск профиля {profile_number}")
        bot = Bot(profile_number, private_key)
        try:
            bot.run_activity()
            print(f"Профиль {profile_number} завершен")
        except Exception as e:
            print(f"Ошибка в профиле {profile_number}, {e}")
        finally:
            bot.close()
    print("Все профили завершены")






if __name__ == '__main__':
    main()

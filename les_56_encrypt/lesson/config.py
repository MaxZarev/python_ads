from pydantic import BaseModel, SecretStr
import keyring


class Config(BaseModel):
    key: SecretStr

config = Config(key=SecretStr(keyring.get_password("encrypt_key", "xxx")))

set_proxy = True
check_proxy = True

salt = 'getpass.getpass("Enter salt: ")'
pin = 'getpass.getpass("Enter pin: ")'
pin_seed = "1-2 3-4 7-8"  # getpass.getpass("Enter pin: ")

# key = getpass.getpass("Enter key: ")
# key_default = getpass.getpass("Enter key: ")  # "_LggSxtOCrjCu8Mt9N0V5tESshRi2EAO1qsKs7xPNqA="

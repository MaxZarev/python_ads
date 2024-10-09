import pathlib

from pydantic import BaseModel, SecretStr
import keyring

class Config(BaseModel):
    key: SecretStr = SecretStr(keyring.get_password("encrypt_key", "xxx"))
    okx_api_key_main: SecretStr = SecretStr(keyring.get_password("okx_api_key", "main"))
    okx_secret_key_main: SecretStr = SecretStr(keyring.get_password("okx_secret_key", "main"))
    okx_passphrase_main: SecretStr = SecretStr(keyring.get_password("okx_passphrase", "main"))

config = Config()

set_proxy = False
check_proxy = False

salt = 'getpass.getpass("Enter salt: ")'
pin = 'getpass.getpass("Enter pin: ")'
pin_seed = "1-2 3-4 7-8"  # getpass.getpass("Enter pin: ")
is_mobile_proxy = False
link_change_ip = ""

metamask_url = "chrome-extension://nkbihfbeogaeaoehlefnkodbefgpgknn/home.html"
excel_path = "path"

rpc = 'https://1rpc.io/arb'
chain = 'Ethereum'

PATH_TO_CONFIG = pathlib.Path(__file__).parent
PATH_TO_DATA = PATH_TO_CONFIG / "data"

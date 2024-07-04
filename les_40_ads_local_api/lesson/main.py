import time

import requests

def check_browser(profile_number: int):
    url = "http://local.adspower.net:50325/api/v1/browser/active"
    parameters = {"serial_number": profile_number}
    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        return response.json()
    else:
        return False


def open_browser(profile_number: int):
    url = "http://local.adspower.net:50325/api/v1/browser/start"
    parameters = {"serial_number": profile_number, "open_tabs": 1}
    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        return True
    else:
        return False

def close_browser(profile_number: int):
    url = "http://local.adspower.net:50325/api/v1/browser/stop"
    parameters = {"serial_number": profile_number}
    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        return True
    else:
        return False


def main():
    open_browser(948)
    result = check_browser(948)
    print(result)





if __name__ == '__main__':
    main()
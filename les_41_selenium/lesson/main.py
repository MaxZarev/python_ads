import time

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def start_profile(profile_number: int) -> webdriver.Chrome:
    profile_data = open_browser(profile_number)
    if profile_data:
        chrome_driver = profile_data["data"]["webdriver"]
        selenium_port = profile_data["data"]["ws"]["selenium"]

        service = Service(executable_path=chrome_driver)

        options = Options()
        options.add_experimental_option("debuggerAddress", selenium_port)
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(options=options, service=service)
        return driver


def close_browser(profile_number: int):
    url = "http://local.adspower.net:50325/api/v1/browser/stop"
    parameters = {"serial_number": profile_number}
    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        return True
    else:
        return False


def open_browser(profile_number: int):
    url = "http://local.adspower.net:50325/api/v1/browser/start"
    parameters = {"serial_number": profile_number, "open_tabs": 1}
    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        return response.json()

def main():
    profiles = [947, 948, 949]
    for num_profile in profiles:
        client = start_profile(num_profile)
        client.get("https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html")
        time.sleep(1)
        close_browser(num_profile)
        time.sleep(1)








if __name__ == '__main__':
    main()
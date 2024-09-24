from web3 import Web3

class Onchain:
    def __init__(self, private_key):
        self.private_key = private_key
        self.w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/"))
        self.address = self.w3.eth.account.from_key(private_key).address


from web3 import Web3
from config import *


def main():
    address = Web3.to_checksum_address('0xac8ce8fbC80115a22a9a69e42f50713AAe9ef2F7')
    w3 = Web3(Web3.HTTPProvider(RPC_ARB))
    wei = w3.eth.get_balance(address)
    print(wei / 10 ** 18)


if __name__ == '__main__':
    main()

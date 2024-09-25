from __future__ import annotations

import json
from decimal import Decimal
from typing import Optional

from eth_typing import ChecksumAddress
from web3 import Web3
from web3.types import Wei

from config import rpc


class Onchain:
    def __init__(self, private_key):
        self.private_key = private_key
        self.w3 = Web3(Web3.HTTPProvider(rpc))
        self.address = self.w3.eth.account.from_key(private_key).address

    def get_balance(self, contract_address: Optional[str | ChecksumAddress] = None) -> Amount:
        if not contract_address:
            balance = Amount(self.w3.eth.get_balance(self.address), wei=True)
        else:
            abi = json.load(open('config/data/ABIs/erc20.json'))
            contract = self.w3.eth.contract(contract_address, abi=abi)
            erc20_balance_wei = contract.functions.balanceOf(self.address).call()
            decimals = contract.functions.decimals().call()
            balance = Amount(erc20_balance_wei, decimals=decimals, wei=True)
        return balance


class Amount:
    wei: int | Wei
    ether: Decimal
    ether_float: float

    def __init__(self, amount: int | float | Decimal | Wei, decimals: int = 18, wei: bool = False):
        if wei:
            self.wei = int(amount)
            self.ether = Decimal(str(amount)) / 10 ** decimals
            self.ether_float = float(self.ether)
        else:
            self.wei = int(amount * 10 ** decimals)
            self.ether = Decimal(str(amount))
            self.ether_float = float(self.ether)

        self.decimals = decimals

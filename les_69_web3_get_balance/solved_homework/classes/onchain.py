from __future__ import annotations

import json
from decimal import Decimal
from typing import Optional

from eth_typing import ChecksumAddress
from web3 import Web3
from web3.contract import Contract
from web3.types import Wei

from config import rpc


class Onchain:
    def __init__(self, private_key):
        self.private_key = private_key
        self.w3 = Web3(Web3.HTTPProvider(rpc))
        self.address = self.w3.eth.account.from_key(private_key).address

    def get_balance(self, contract_address: Optional[str | ChecksumAddress] = None) -> Amount:
        """
        Получение баланса кошелька, в формате Amount
        :param contract_address: адрес смарт контракта в блокчейне, если не указан, то нативный баланс
        :return: объект Amount с балансом
        """
        if not contract_address:
            balance = Amount(self.w3.eth.get_balance(self.address), wei=True)
        else:
            contract = self.get_contract(contract_address, 'erc20')
            erc20_balance_wei = contract.functions.balanceOf(self.address).call()
            decimals = contract.functions.decimals().call()
            balance = Amount(erc20_balance_wei, decimals=decimals, wei=True)
        return balance

    def get_contract(self, contract_address: str, abi_name: str) -> Contract:
        """
        Получение объекта контракта, по адресу и названию ABI
        :param contract_address: адрес смарт контракта в блокчейне
        :param abi_name: название файла с ABI без расширения
        :return: инициализированный объект контракта
        """
        if isinstance(contract_address, str):
            contract_address = self.w3.to_checksum_address(contract_address)
        abi = json.load(open(f'config/data/ABIs/{abi_name}.json'))
        contract = self.w3.eth.contract(contract_address, abi=abi)
        return contract


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

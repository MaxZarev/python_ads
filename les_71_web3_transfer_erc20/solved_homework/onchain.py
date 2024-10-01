from __future__ import annotations

import json
import random
from decimal import Decimal
from typing import Optional

from eth_typing import ChecksumAddress
from web3 import Web3
from web3.contract import Contract
from web3.contract.contract import ContractFunction
from web3.types import Wei
from web3 import utils

from config import rpc, PATH_TO_DATA


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
        abi = json.load(open(PATH_TO_DATA / f'ABIs/{abi_name}.json'))
        contract = self.w3.eth.contract(contract_address, abi=abi)
        return contract

    def get_priority_fee(self) -> int:
        """
        Получение приоритетной ставки для транзакции за последние 30 блоков
        :return: приоритетная ставка
        """
        fee_history = self.w3.eth.fee_history(30, 'latest', [20])
        priority_fees = [priority_fee[0] for priority_fee in fee_history['reward']]
        median_index = len(priority_fees) // 2
        priority_fees.sort()
        median_priority_fee = priority_fees[median_index]
        random_multiplier = random.uniform(1.05, 1.1)
        return int(median_priority_fee * random_multiplier)

    def send_token(self, amount: Amount, to_address: str | ChecksumAddress,
                   token_contract: Optional[str, ChecksumAddress] = None) -> str:
        """
        Отправка любых типов токенов, если не указан адрес контракта, то отправка нативного токена
        :param amount: объект Amount с суммой
        :param to_address: адрес получателя
        :param token_contract: адрес смарт контракта токена
        :return: хэш транзакции
        """
        if isinstance(to_address, str):
            to_address = self.w3.to_checksum_address(to_address)

        balance = self.get_balance(token_contract)
        random_multiplier = random.uniform(1.05, 1.1)

        if token_contract:
            if balance.wei < amount.wei:
                amount = balance
            contract = self.get_contract(token_contract, 'erc20')
            tx_params = self.prepare_tx()
            tx = contract.functions.transfer(to_address, amount.wei).build_transaction(tx_params)
        else:
            tx = self.prepare_tx(amount, to_address)
            if balance.wei < amount.wei:
                tx['value'] = int(balance.wei - tx['maxFeePerGas'] * 100000)

        tx['gas'] = int(self.w3.eth.estimate_gas(tx) * random_multiplier * 1.1)
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt.transactionHash.hex()

    def prepare_tx(self, value: Optional[Amount] = None,
                   to_address: Optional[str | ChecksumAddress] = None) -> dict:
        """
        Подготовка параметров транзакции
        :param value: сумма перевода ETH, если ETH нужно приложить к транзакции
        :param to_address:  адрес получателя, если транзакция НЕ на смарт контракт
        :return: параметры транзакции
        """
        random_multiplier = random.uniform(1.05, 1.1)
        base_fee = self.w3.eth.gas_price
        priority_fee = self.get_priority_fee()
        max_fee = int((base_fee + priority_fee) * random_multiplier)

        tx_params = {
            'from': self.address,
            'nonce': self.w3.eth.get_transaction_count(self.address),
            'maxFeePerGas': max_fee,
            'maxPriorityFeePerGas': priority_fee,
            'chainId': self.w3.eth.chain_id,
        }

        if value:
            tx_params['value'] = value.wei

        if to_address:
            tx_params['to'] = to_address

        return tx_params


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


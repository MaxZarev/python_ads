from __future__ import annotations

import json
import random
from decimal import Decimal
from typing import Optional

from eth_typing import ChecksumAddress
from web3 import Web3
from web3.contract import Contract
from web3.types import Wei

from config import rpc, PATH_TO_DATA


class Onchain:
    def __init__(self, private_key: str, rpc: str):
        self.private_key = private_key
        self.w3 = Web3(Web3.HTTPProvider(rpc))
        self.address = self.w3.eth.account.from_key(private_key).address

    def get_balance(self, token: Optional[Token] = None,
                    token_contract: Optional[str | ChecksumAddress] = None) -> Amount:
        """
        Получение баланса кошелька, в формате Amount
        :param token: объект Token
        :param token_contract: адрес смарт контракта токена, если не указан, то нативный баланс
        :return: объект Amount с балансом
        """
        if token_contract and not token:
            token = Token('token', token_contract)

        if token == Tokens.ETH or not token:
            balance = Amount(self.w3.eth.get_balance(self.address), wei=True)
        else:
            contract = self.get_contract(token)
            erc20_balance_wei = contract.functions.balanceOf(self.address).call()
            if token.name == 'token':
                token.decimals = contract.functions.decimals().call()
            balance = Amount(erc20_balance_wei, decimals=token.decimals, wei=True)
        return balance

    def get_contract(self, contract_raw: Optional[ContractRaw | Token] = None,
                     contract_address: Optional[str] = None,
                     abi_name: Optional[str] = None) -> Contract:
        """
        Получение объекта контракта, по адресу и названию ABI
        :param contract_address: адрес смарт контракта в блокчейне
        :param abi_name: название файла с ABI без расширения
        :return: инициализированный объект контракта
        """
        if contract_raw:
            contract_address = contract_raw.address
            abi_name = contract_raw.name
            if isinstance(contract_raw, Token):
                abi_name = 'erc20'

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

        hash = self.sing_and_send(tx)
        message = f'send {amount.ether_float} {token_contract.name if token_contract else "ETH"}'
        print(f'Транзакция отправлена {message} to {to_address} tx hash: {hash}')
        return hash

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

    def _replace_eth_with_weth(self, token: Token) -> Token:
        """
        Замена ETH на WETH для поиска пула ликвидности
        :param token: объект Token
        :return: исходный объект Token или WETH вместо ETH
        """
        if token == Tokens.ETH:
            return Tokens.WETH
        return token

    def swap(self, src_token: Token, dst_token: Token, amount: Amount | int | float) -> Optional[str]:
        """
        Обмен через arbswap
        :param src_token: токен из которого делаем обмен
        :param dst_token: токен в который делаем обмен
        :param amount: сумма обмена
        :return: хэш транзакции
        """

        # приводим сумму к объекту Amount
        if isinstance(amount, (int, float)):
            amount = Amount(amount, decimals=src_token.decimals)

        balance = self.get_balance(src_token)
        if balance.wei < amount.wei:
            print(f'Not enough balance: {balance.ether_float} {src_token.name}')
            return

        if src_token != Tokens.ETH:
            if self.get_allowance(src_token, Contracts.ARBSWAP_UNI_ROUTER).wei < amount.wei:
                self.approve(src_token, amount, Contracts.ARBSWAP_UNI_ROUTER)

        if src_token.type == TokenTypes.STABLE and dst_token.type == TokenTypes.STABLE:
            tx = self._build_stable_swap(src_token, dst_token, amount)
        else:
            tx = self._build_swap_tx(src_token, dst_token, amount)

        hash = self.sing_and_send(tx)
        message = f'swap {amount.ether_float} {src_token.name} to {dst_token.name}'
        print(f'Транзакция отправлена {message} tx hash: {hash}')
        return hash

    def _build_stable_swap(self, src_token: Token, dst_token: Token, amount: Amount | int | float) -> \
            Optional[dict]:
        """
        Построение транзакции обмена стейблкоинов
        :param src_token: исходный стейблкоин
        :param dst_token: целевой стейблкоин
        :param amount: сумма обмена
        :return: параметры транзакции
        """

        min_return = Amount(amount.wei * 0.95, decimals=dst_token.decimals, wei=True)
        # подготавливаем транзакцию
        tx_params = self.prepare_tx()
        contract = self.get_contract(Contracts.ARBSWAP_UNI_ROUTER)
        tx = contract.functions.swap(
            src_token.address,
            dst_token.address,
            amount.wei,
            min_return.wei,
            0
        ).build_transaction(tx_params)
        return tx

    def _build_swap_tx(self, src_token: Token, dst_token: Token, amount: Amount | int | float) -> Optional[
        str]:
        """
        Построение транзакции обмена токенов
        :param src_token: исходный токен
        :param dst_token: целевой токен
        :param amount: сумма обмена
        :return: параметры транзакции
        """
        # подменяем ETH на WETH для поиска пула ликвидности
        _src_token = self._replace_eth_with_weth(src_token)
        _dst_token = self._replace_eth_with_weth(dst_token)

        # получаем адрес пула ликвидности
        swap_factory_contract = self.get_contract(Contracts.ARBSWAP_SWAP_FACTORY)
        pool_contract_address = swap_factory_contract.functions.getPair(
            _src_token.address,
            _dst_token.address
        ).call()

        # получаем резервы пула ликвидности и считаем цену обмена
        pool_contract = self.get_contract(contract_address=pool_contract_address,
                                          abi_name='arbswap_swap_pair')
        reserve0, reserve1, _ = pool_contract.functions.getReserves().call()
        if int(_src_token.address, 16) > int(_dst_token.address, 16):
            reserve0, reserve1 = reserve1, reserve0
        change_price = reserve1 / reserve0
        amount_out = amount.wei * change_price * 0.947
        min_return = Amount(amount_out, decimals=dst_token.decimals, wei=True)

        # подготавливаем транзакцию
        tx_params = self.prepare_tx(value=amount if src_token == Tokens.ETH else None)
        contract = self.get_contract(Contracts.ARBSWAP_UNI_ROUTER)
        tx = contract.functions.swap(
            src_token.address,
            dst_token.address,
            amount.wei,
            min_return.wei,
            1
        ).build_transaction(tx_params)
        return tx

    def get_allowance(self, token: Token, spender: str | ChecksumAddress | ContractRaw) -> Amount:
        """
        Получение разрешенной суммы токенов на снятие
        :param token: объект Token
        :param spender: адрес контракта, который получил разрешение на снятие токенов
        :return: объект Amount с разрешенной суммой
        """
        if isinstance(spender, ContractRaw):
            spender = spender.address

        if isinstance(spender, str):
            spender = Web3.to_checksum_address(spender)

        contract = self.get_contract(token)
        allowance = contract.functions.allowance(self.address, spender).call()
        return Amount(allowance, decimals=token.decimals, wei=True)

    def approve(self, token: Token, amount: Amount | int | float,
                spender: str | ChecksumAddress | ContractRaw) -> None:

        """
        Одобрение транзакции на снятие токенов
        :param token: токен, который одобряем
        :param amount: сумма одобрения
        :param spender: адрес контракта, который получит разрешение на снятие токенов
        :return: None
        """

        if isinstance(amount, (int, float)):
            amount = Amount(amount, decimals=token.decimals)

        if isinstance(spender, ContractRaw):
            spender = spender.address

        contract = self.get_contract(token)
        tx_params = self.prepare_tx()

        tx = contract.functions.approve(spender, amount.wei).build_transaction(tx_params)
        self.sing_and_send(tx)
        message = f'approve {amount.ether_float} {token.name} to {spender}'
        print(f'Транзакция отправлена {message}')

    def sing_and_send(self, tx: dict) -> str:
        """
        Подпись и отправка транзакции
        :param tx: параметры транзакции
        :return: хэш транзакции
        """
        random_multiplier = random.uniform(1.05, 1.1)
        tx['gas'] = int(self.w3.eth.estimate_gas(tx) * random_multiplier * 1.1)
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt.transactionHash.hex()


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


class TokenTypes:
    ERC20 = 'erc20'
    NATIVE = 'native'
    STABLE = 'stable'


class ContractRaw:
    def __init__(self, name: str, address: str | ChecksumAddress):
        self.name = name
        self.address = Web3.to_checksum_address(address)


class Contracts:
    ARBSWAP_SWAP_FACTORY = ContractRaw('arbswap_swap_factory', '0xd394e9cc20f43d2651293756f8d320668e850f1b')
    ARBSWAP_UNI_ROUTER = ContractRaw('arbswap_uni_router', '0x6947a425453d04305520e612f0cb2952e4d07d62')
    ARBSWAP_STABLE_SWAP_FACTORY = ContractRaw('arbswap_stable_swap_factory',
                                              '0x3a52e9200Ed7403D9d21664fDee540C2d02c099d')


class Token:
    def __init__(self, name: str, address: str | ChecksumAddress, decimals: int = 18,
                 type: str = TokenTypes.ERC20):
        self.name = name
        self.address = Web3.to_checksum_address(address)
        self.decimals = decimals
        self.type = type


class Tokens:
    ETH = Token('ETH', '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee', type=TokenTypes.NATIVE)
    WETH = Token('WETH', '0x82aF49447D8a07e3bd95BD0d56f35241523fBab1', decimals=18, type=TokenTypes.ERC20)
    USDC = Token('USDC', '0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8', decimals=6, type=TokenTypes.STABLE)
    USDT = Token('USDT', '0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9', decimals=6, type=TokenTypes.STABLE)


if __name__ == '__main__':
    pk = ''
    onchain = Onchain(pk, rpc=rpc)
    onchain.swap(Tokens.USDC, Tokens.ETH, 1)
    pass
    #
    # allowance = {
    #     'sender': {
    #         'resepient': 50,
    #         'адрес_кто_баланс_тратит_2': 100
    #     }
    # }

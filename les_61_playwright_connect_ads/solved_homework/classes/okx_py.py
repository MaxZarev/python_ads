from __future__ import annotations

from pprint import pprint
from typing import TYPE_CHECKING
import keyring

from config import config

import okx.SubAccount as SubAccount
import okx.Funding as Funding
import okx.Account as Account

from utils import sleep_random

if TYPE_CHECKING:
    from classes.ads import Ads


class OKX:
    def __init__(self, ads: Ads):
        self.ads = ads
        self.sub_account_api = SubAccount.SubAccountAPI(
            config.okx_api_key_main.get_secret_value(),
            config.okx_secret_key_main.get_secret_value(),
            config.okx_passphrase_main.get_secret_value(),
            flag="0",
            debug=False
        )
        self.funding_api = Funding.FundingAPI(
            config.okx_api_key_main.get_secret_value(),
            config.okx_secret_key_main.get_secret_value(),
            config.okx_passphrase_main.get_secret_value(),
            flag="0",
            debug=False
        )

    def collect_sub_balances(self):
        sub_list_response = self.sub_account_api.get_subaccount_list()
        sub_list = sub_list_response["data"]
        for sub in sub_list:
            sub_name = sub["subAcct"]
            balance = self.sub_account_api.get_funding_balance(sub_name)
            if balance["data"]:
                balances = balance["data"]

                funding_api = Funding.FundingAPI(
                    keyring.get_password("okx_api_key", sub_name),
                    keyring.get_password("okx_secret_key", sub_name),
                    keyring.get_password("okx_passphrase", sub_name),
                    flag="0",
                    debug=False
                )

                for balance in balances:
                    token_name = balance["ccy"]
                    token_amount = balance["availBal"]
                    response = funding_api.funds_transfer(
                        ccy=token_name,
                        amt=token_amount,
                        from_="6",
                        to="6",
                        type='3',
                        subAcct=sub_name
                    )
                    print(f"Вывод с суб аккаунта {response}")

    def withdrawal(self, token_name: str, amount: float | int | str, chain: str, address: str = ""):
        """
        Вывод токена с основного аккаунта с ожиданием
        :param token_name: тикер токена
        :param amount: количество токенов
        :param chain: сеть вывода
        :param address: адрес вывода, если отличается от адреса аккаунта
        :return:
        """
        # приводим тип данных к str
        if isinstance(amount, (float, int)):
            amount = str(amount)

        # если не передавали адрес, используем адрес из объекта ads
        if not address:
            address = self.ads.address

        # запрашиваем комиссию
        fee = self.get_fee(token_name, chain)

        # отправляем запрос на вывод
        response = self.funding_api.withdrawal(
            ccy=token_name,
            amt=amount,
            dest="4",
            toAddr=address,
            fee=fee,
            chain=f"{token_name}-{chain}"
        )

        # если статус не 0, выводим сообщение и рейзим ошибку
        if response["code"] != "0":
            pprint(response)
            raise Exception("Ошибка вывода")

        # получаем айди вывода, чтобы отследить статус
        withdraw_id = response["data"]['wdId']

        # отслеживаем статус
        for _ in range(30):
            status = self.funding_api.get_deposit_withdraw_status(withdraw_id)
            if status["data"]["state"] == "Withdrawal complete":
                print("Вывод завершен")
                return
            sleep_random(5, 10)


    def get_fee(self, token_name: str, chain: str) -> str:
        """
        Получение комиссии для вывода токена
        :param token_name: тикер токена
        :param chain: сеть токена
        :return: строчка с суммой комиссии
        """
        response = self.funding_api.get_currencies(token_name)
        network = f"{token_name}-{chain}"
        for chain_data in response['data']:
            if chain_data['chain'] == network:
                return chain_data['minFee']


if __name__ == '__main__':
    ex = OKX(None)
    response = ex.funding_api.get_deposit_withdraw_status("219704826")
    print(response)


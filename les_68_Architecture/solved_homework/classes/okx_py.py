from __future__ import annotations

from typing import Literal

import keyring

from config import config

import okx.SubAccount as SubAccount
import okx.Funding as Funding

from utils import random_sleep


class OKX:
    def __init__(self):
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

    def withdraw(
            self,
            address: str,
            chain: Literal["ERC20", "Linea"],
            token: str,
            amount: float
    ) -> None:
        """
        Вывод средств с биржи OKX
        :param address:  Адрес кошелька
        :param chain: сеть
        :param token: токен
        :param amount: сумма
        :return: None
        """
        token_with_chain = token + "-" + chain
        fee = self._get_withdrawal_fee(token, token_with_chain)

        try:
            print(f'{address}: Выводим с okx {amount} {token}')
            response = self.funding_api.withdrawal(
                ccy=token,
                amt=amount,
                dest=4,
                toAddr=address,
                fee=fee,
                chain=token_with_chain,
            )
            if response.get("code") != "0":
                raise Exception(
                    f'{address}: Не удалось вывести {amount} {token}: {response.get("msg")}')
            tx_id = response.get("data")[0].get("wdId")
            self.wait_confirm(tx_id)
            print(f'{address}: Успешно выведено {amount} {token}')
        except Exception as error:
            print(f'{address}: Не удалось вывести {amount} {token}: {error} ')
            raise error

    def _get_withdrawal_fee(self, token: str, token_with_chain: str):
        """
        Получение комиссии за вывод
        :param token: название токена
        :param token_with_chain: айди токен-сеть
        :return:
        """
        response = self.funding_api.get_currencies(token)
        for network in response.get("data"):
            if network.get("chain") == token_with_chain:
                return network.get("minFee")

        print(f" не могу получить сумму комиссии, проверьте значения symbolWithdraw и network")
        return 0

    async def wait_confirm(self, tx_id: str) -> None:
        """
        Ожидание подтверждения транзакции вывода с OKX
        :param tx_id: id транзакции вывода
        :return: None
        """
        for _ in range(30):
            tx_info = self.funding_api.get_deposit_withdraw_status(wdId=tx_id)
            if tx_info.get("code") == "0":
                if 'Withdrawal complete' in tx_info.get("data")[0].get("state"):
                    print(f"Транзакция {tx_id} завершена")
                    return
            random_sleep(10)
        print(f"Ошибка транзакция {tx_id} не завершена")
        raise Exception(f"Транзакция {tx_id} не завершена")



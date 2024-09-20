from __future__ import annotations

import keyring

from config import config

import okx.SubAccount as SubAccount
import okx.Funding as Funding


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


if __name__ == '__main__':
    pass


import datetime as dt
from json import JSONDecodeError
import json


def load_wallets():
    try:
        with open("wallets.json", "r") as f:
            local_wallets_list = json.load(f)

    except JSONDecodeError:
        local_wallets_list = []
    return local_wallets_list


def save_to_json(wallet):
    wallets_list = load_wallets()
    wallets_dict_list = []
    for wallet_dict in wallets_list:
        wallet_obj = Wallet(**wallet_dict)
        if wallet_obj.name == wallet.name:
            wallet_obj.current_amount = wallet.current_amount
            wallet_obj.withdraw_history = wallet.withdraw_history
            wallet_obj.deposit_history = wallet.deposit_history
        wallet_dict = wallet_obj.__dict__
        wallets_dict_list.append(wallet_dict)

    with open("wallets.json", "w") as f:
        json.dump(wallets_dict_list, f)


class Wallet:
    def __init__(self, current_amount, name, withdraw_history, deposit_history):
        self.current_amount = current_amount
        self.name = name
        self.withdraw_history = withdraw_history
        self.deposit_history = deposit_history

    def withdraw(self, withdraw_amount, category):
        if self.current_amount < withdraw_amount:
            raise ValueError
        self.current_amount -= withdraw_amount
        current_withdraw_dict = {"time": str(dt.datetime.now()), "amount": withdraw_amount, "category": category}
        self.withdraw_history.append(current_withdraw_dict)

    def deposit(self, deposit_amount):
        self.current_amount += deposit_amount
        current_deposit_dict = {"time": str(dt.datetime.now()), "amount": deposit_amount}
        self.deposit_history.append(current_deposit_dict)

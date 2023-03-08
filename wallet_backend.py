
class Wallet:
    def __init__(self, current_amount, name):
        self.current_amount = current_amount
        self.name = name

    def withdraw(self, withdraw_amount):
        self.current_amount -= withdraw_amount
        print(self.current_amount)

    def deposit(self, deposit_amount):
        self.current_amount += deposit_amount
        print(self.current_amount)


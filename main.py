import tkinter as tk

class BankUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Bank App")
        self.master.geometry("400x400")
        self.master.configure(bg="#FF6666")

        self.label1 = tk.Label(self.master, text="Welcome to our Bank App!", font=("Arial", 20), bg="#FF6666", fg="#FFFFFF")
        self.label1.pack(pady=20)

        self.label2 = tk.Label(self.master, text="Your balance:", font=("Arial", 14), bg="#FF6666", fg="#FFFFFF")
        self.label2.pack(pady=10)

        self.balance = tk.Label(self.master, text="$0", font=("Arial", 18), bg="#FF6666", fg="#FFFFFF")
        self.balance.pack(pady=10)

        self.deposit_button = tk.Button(self.master, text="Deposit", font=("Arial", 14), bg="#FFFFFF", fg="#FF6666", command=self.deposit)
        self.deposit_button.pack(pady=10)

        self.withdraw_button = tk.Button(self.master, text="Withdraw", font=("Arial", 14), bg="#FFFFFF", fg="#FF6666", command=self.withdraw)
        self.withdraw_button.pack(pady=10)

        self.quit_button = tk.Button(self.master, text="Quit", font=("Arial", 14), bg="#FFFFFF", fg="#FF6666", command=self.quit)
        self.quit_button.pack(pady=20)

    def deposit(self):
        amount = float(input("How much would you like to deposit? "))
        balance = float(self.balance["text"].replace("$", ""))
        new_balance = balance + amount
        self.balance["text"] = "${:.2f}".format(new_balance)

    def withdraw(self):
        amount = float(input("How much would you like to withdraw? "))
        balance = float(self.balance["text"].replace("$", ""))
        if amount > balance:
            print("Insufficient funds.")
        else:
            new_balance = balance - amount
            self.balance["text"] = "${:.2f}".format(new_balance)

    def quit(self):
        self.master.destroy()

import json

def load_wallets():
    try:
        with open("wallets.json", "r") as f:
            wallets = json.load(f)
    except FileNotFoundError:
        wallets = {"Checking": 0, "Savings": 0}
    return wallets

def save_wallets(wallets):
    with open("wallets.json", "w") as f:
        json.dump(wallets, f)

def deposit(wallets):
    print("Select a wallet to deposit into:")
    for wallet in wallets:
        print(wallet)
    selected_wallet = input(">")
    if selected_wallet in wallets:
        amount = float(input("Enter amount to deposit: "))
        wallets[selected_wallet] += amount
        print("Deposited ${:.2f} into {}.".format(amount, selected_wallet))
        save_wallets(wallets)
    else:
        print("Invalid wallet selected.")

def withdraw(wallets):
    print("Select a wallet to withdraw from:")
    for wallet in wallets:
        print(wallet)
    selected_wallet = input(">")
    if selected_wallet in wallets:
        amount = float(input("Enter amount to withdraw: "))
        if amount > wallets[selected_wallet]:
            print("Insufficient funds.")
        else:
            wallets[selected_wallet] -= amount
            print("Withdrew ${:.2f} from {}.".format(amount, selected_wallet))
            save_wallets(wallets)
    else:
        print("Invalid wallet selected.")

def check_balance(wallets):
    print("Select a wallet to check balance:")
    for wallet in wallets:
        print(wallet)
    selected_wallet = input(">")
    if selected_wallet in wallets:
        print("${:.2f} in {}.".format(wallets[selected_wallet], selected_wallet))
    else:
        print("Invalid wallet selected.")

wallets = load_wallets()

while True:
    print("Select an option:")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Check balance")
    print("4. Quit")
    choice = input(">")
    if choice == "1":
        deposit(wallets)
    elif choice == "2":
        withdraw(wallets)
    elif choice == "3":
        check_balance(wallets)
    elif choice == "4":
        break
    else:
        print("Invalid choice.")


if __name__ == '__main__':
    root = tk.Tk()
    my_gui = BankUI(root)
    root.mainloop()


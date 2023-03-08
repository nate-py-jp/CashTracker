import tkinter as tk
from wallet_backend import Wallet
import json
from json import JSONDecodeError

# TODO: let you choose the type of money being used with an api
# TODO: let you convert your wallet to other money
# TODO: let you automatically deposit or withdraw from images of receipts
# TODO: make modern-looking UI
# TODO: make it so you can't go below 0
# TODO: make a pop up that verifies the amount you will deposit or withdraw
# TODO: refactor for repetition
# TODO: test the code
# TODO: give you categories for the spent money
# TODO: display the categories of spent money in a pie chart with pandas/seaborn


# create wallet, root
root = tk.Tk()
root.title("CashTracker")

# declare global variable(s) - to be in functions
global deposit_entry, withdraw_entry, name_entry


# non-tk functions
def load_wallets():
    try:
        with open("wallets.json", "r") as f:
            local_wallets_list = json.load(f)

    except JSONDecodeError:
        local_wallets_list = []
    return local_wallets_list


def add_commas(event):
    # Get the current text in the Entry widget
    current_nums = event.widget.get()

    # Convert the numbers to numbers with
    if "," in current_nums:
        current_nums = current_nums.replace(",", "")
    nums_with_commas = f"{int(current_nums):,}"

    # Insert the modified text back into the Entry widget
    event.widget.delete(0, tk.END)
    event.widget.insert(0, nums_with_commas)


# tk functions
def welcome_screen(previous_screen=None):

    if previous_screen:
        previous_screen.forget()

    # create canvas
    canvas = tk.Canvas(root, width=400, height=300)

    # create widgets
    welcome_label = tk.Label(text="Welcome! Let's track your spending.")
    new_wallet_button = tk.Button(text="create new wallet", command=lambda: create_new_wallet_screen(canvas))
    existing_wallet_button = tk.Button(text="use existing wallet", command=lambda: existing_wallet_screen(canvas))

    # put widgets on canvas
    canvas.create_window(200, 20, window=welcome_label)
    canvas.create_window(280, 100, window=new_wallet_button)
    canvas.create_window(120, 100, window=existing_wallet_button)

    # put canvas on screen
    canvas.pack()


def existing_wallet_screen(previous_screen):

    previous_screen.delete("all")

    # create canvas
    canvas = tk.Canvas(root, width=400, height=300)

    # create widgets
    name_label = tk.Label(text="Choose from the following wallets:")

    wallets_dicts = load_wallets()
    if not wallets_dicts:
        no_wallets_label = tk.Label(text="There are no wallets. Go back")
        canvas.create_window(200, 200, window=no_wallets_label)

    wallet_heights = 30

    for wallet in wallets_dicts:
        wallet_object = Wallet(**wallet)
        print(wallet_object.name, wallet_object.current_amount)
        wallet_button = tk.Button(
            text=f"{wallet_object.name}",
            command=lambda w=Wallet(**wallet): main_screen(
                previous_canvas=canvas,
                wallet=w)
            )
        canvas.create_window(320, wallet_heights, window=wallet_button)
        wallet_heights += 30

    back_button = tk.Button(
        text="Back",
        command=lambda: welcome_screen(previous_screen=canvas)
        )

    # put widgets on the canvas
    canvas.create_window(150, 100, window=name_label)
    canvas.create_window(250, 250, window=back_button)

    # put canvas on the screen
    canvas.pack()
    previous_screen.forget()


def create_new_wallet_screen(previous_screen):

    global name_entry
    previous_screen.delete("all")

    # create canvas
    canvas = tk.Canvas(root, width=400, height=300)

    # create widgets
    name_label = tk.Label(text="Enter a name for the new wallet:")
    name_entry = tk.Entry()
    name_button = tk.Button(
        text="Create",
        command=lambda: main_screen(
            previous_canvas=canvas,
            wallet=create_new_wallet()
        )
    )

    back_button = tk.Button(
        text="Back",
        command=lambda: welcome_screen(previous_screen=canvas)
    )
    print(name_entry.get())

    # put widgets on the canvas
    canvas.create_window(250, 250, window=back_button)
    canvas.create_window(150, 100, window=name_label)
    canvas.create_window(150, 150, window=name_entry)
    canvas.create_window(300, 150, window=name_button)

    # put canvas on the screen
    canvas.pack()
    previous_screen.forget()


def main_screen(wallet, previous_canvas=None):

    print(wallet, wallet.name, wallet.current_amount)

    # delete previous screen
    if previous_canvas:
        previous_canvas.delete("all")

    # create canvas
    canvas = tk.Canvas(root, width=400, height=300)

    # create widgets
    deposit_button = tk.Button(
        text="deposit",
        command=lambda: deposit_screen(
            wallet,
            canvas,
            )
    )
    withdraw_button = tk.Button(
        text="withdraw",
        command=lambda: withdraw_screen(
            canvas,
            wallet=wallet)
    )

    back_button = tk.Button(
        text="Back",
        command=lambda: welcome_screen(previous_screen=canvas)
    )

    # put widgets on canvas
    canvas.create_window(250, 250, window=back_button)
    canvas.create_window(250, 100, window=withdraw_button)
    canvas.create_window(150, 100, window=deposit_button)

    # clear previous screen
    if previous_canvas:
        previous_canvas.pack_forget()

    # put canvas on screen
    canvas.pack()

    # update welcome label
    update_welcome(canvas, wallet)


def deposit_screen(wallet, previous_canvas):

    # declare global variable(s)
    global deposit_entry

    # create canvas
    canvas = tk.Canvas(root, width=400, height=300)

    # create widgets for deposit screen
    deposit_label = tk.Label(canvas, text="Enter deposit amount:")
    deposit_entry = tk.Entry(canvas)
    deposit_entry_button = tk.Button(
        canvas,
        text="Enter",
        command=lambda: (
            deposit(wallet=wallet),
            main_screen(
                previous_canvas=canvas,
                wallet=wallet
            )
        )
    )

    deposit_entry.bind("<KeyRelease>", add_commas)

    # display widgets on screen
    canvas.create_window(200, 20, window=deposit_label)
    canvas.create_window(200, 80, window=deposit_entry)
    canvas.create_window(350, 80, window=deposit_entry_button)

    # put canvas on screen
    previous_canvas.pack_forget()
    canvas.pack()

    # update welcome label
    update_welcome(canvas, wallet)


def withdraw_screen(previous_canvas=None, wallet=None):

    # declare global variable(s)
    global withdraw_entry

    # create canvas
    canvas = tk.Canvas(root, width=400, height=300)

    # create widgets
    withdraw_label = tk.Label(text="Enter withdraw amount:")
    withdraw_entry = tk.Entry(canvas)
    withdraw_entry_button = tk.Button(
        canvas,
        text="Enter",
        command=lambda: (
            withdraw(wallet=wallet),
            main_screen(
                previous_canvas=canvas,
                wallet=wallet))
    )

    withdraw_entry.bind("<KeyRelease>", add_commas)

    # display widgets on screen
    canvas.create_window(200, 20, window=withdraw_label)
    canvas.create_window(200, 80, window=withdraw_entry)
    canvas.create_window(350, 80, window=withdraw_entry_button)

    # put canvas on screen
    previous_canvas.pack_forget()
    canvas.pack()

    # update welcome label
    update_welcome(canvas, wallet)


def update_welcome(canvas, wallet):

    # create welcome widget
    welcome = tk.Label(text=f"{wallet.name} has ¥{wallet.current_amount:,.2f}")

    # put widget on screen
    canvas.create_window(200, 50, window=welcome)


def create_new_wallet():

    wallet_name = name_entry.get()
    wallet = Wallet(0, wallet_name)
    try:
        with open("wallets.json", "r") as f:
            wallet_dicts = json.load(f)

    except JSONDecodeError as e:
        wallet_dicts = []

    wallet_dicts.append(wallet.__dict__)

    with open("wallets.json", "w") as f:
        json.dump(wallet_dicts, f)

    return wallet


def deposit(wallet):

    amount = float(deposit_entry.get().replace(",", ""))
    wallet.deposit(amount)

    # save deposit to json
    wallets_list = load_wallets()
    wallets_dict_list = []
    for wallet_dict in wallets_list:
        wallet_obj = Wallet(**wallet_dict)
        print(wallet_obj.name)
        if wallet_obj.name == wallet.name:
            wallet_obj.current_amount = wallet.current_amount
            print(wallet_obj.current_amount)
        wallet_dict = wallet_obj.__dict__
        wallets_dict_list.append(wallet_dict)
    with open("wallets.json", "w") as f:
        json.dump(wallets_dict_list, f)

    return wallet


def withdraw(wallet):

    amount = float(withdraw_entry.get().replace(",", ""))
    wallet.withdraw(amount)

    # save deposit to json
    wallets_list = load_wallets()
    wallets_dict_list = []
    for wallet_dict in wallets_list:
        wallet_obj = Wallet(**wallet_dict)
        print(wallet_obj.name)
        if wallet_obj.name == wallet.name:
            wallet_obj.current_amount = wallet.current_amount
            print(wallet_obj.current_amount)
        wallet_dict = wallet_obj.__dict__
        wallets_dict_list.append(wallet_dict)
    with open("wallets.json", "w") as f:
        json.dump(wallets_dict_list, f)

    return wallet


welcome_screen()
root.mainloop()

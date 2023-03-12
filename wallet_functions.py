import tkinter as tk
from wallet_backend import Wallet, load_wallets, save_to_json
import json

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
# TODO: move json stuff to wallet_backend


# create wallet, root
root = tk.Tk()
root.title("CashTracker")

# declare global variable(s) - to be in functions
global deposit_entry, withdraw_entry, name_entry, deposit_category_chooser, withdraw_category_chooser


# helper functions
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

    history_button = tk.Button(
        text="history",
        command=lambda: history_screen(
            previous_canvas=canvas,
            wallet=wallet
        )
    )

    back_button = tk.Button(
        text="Back",
        command=lambda: welcome_screen(previous_screen=canvas)
    )

    # put widgets on canvas
    canvas.create_window(250, 250, window=back_button)
    canvas.create_window(250, 100, window=withdraw_button)
    canvas.create_window(150, 100, window=deposit_button)
    canvas.create_window(350, 100, window=history_button)

    # clear previous screen
    if previous_canvas:
        previous_canvas.pack_forget()

    # put canvas on screen
    canvas.pack()

    # update welcome label
    update_welcome(canvas, wallet)


def history_screen(wallet, previous_canvas):

    # create canvas
    canvas = tk.Canvas(root, width=400, height=300)

    # create widgets
    key_label = tk.Label(text="AMOUNT / TIME / CATEGORY", font=("Helvetica", 16, "bold"))
    back_button = tk.Button(
        text="Back",
        command=lambda: main_screen(wallet=wallet, previous_canvas=canvas)
    )

    history_height = 50

    for action in wallet.withdraw_history:
        action_label = tk.Label(text=f"{action['amount']} / {action['time']} / {action['category']}")
        canvas.create_window(200, history_height, window=action_label)
        history_height += 20

    # put widgets on canvas
    canvas.create_window(200, 30, window=key_label)
    canvas.create_window(250, 250, window=back_button)

    previous_canvas.forget()

    canvas.pack()


def deposit_screen(wallet, previous_canvas):

    # declare global variable(s)
    global deposit_entry, deposit_category_chooser

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

    items = ["other", "snacks and drinks", "lunch bentos", "weekends"]
    list_items = tk.Variable(value=items)
    deposit_category_label = tk.Label(canvas, text="Choose a category: ")
    deposit_category_chooser = tk.Listbox(canvas, height=5, width=10, listvariable=list_items,selectmode=tk.SINGLE)

    deposit_entry.bind("<KeyRelease>", add_commas)
    deposit_category_chooser.bind('<<ListboxSelect>>', lambda x: x)

    # display widgets on screen
    canvas.create_window(200, 20, window=deposit_label)
    canvas.create_window(200, 80, window=deposit_entry)
    canvas.create_window(350, 80, window=deposit_entry_button)
    canvas.create_window(100, 200, window=deposit_category_label)
    canvas.create_window(250, 200, window=deposit_category_chooser)

    # put canvas on screen
    previous_canvas.pack_forget()
    canvas.pack()

    # update welcome label
    update_welcome(canvas, wallet)


def withdraw_screen(previous_canvas=None, wallet=None):

    # declare global variable(s)
    global withdraw_entry, withdraw_category_chooser

    # create canvas
    canvas = tk.Canvas(root, width=400, height=300)

    # create widgets
    withdraw_label = tk.Label(text="Enter withdraw amount:")
    withdraw_entry = tk.Entry(canvas)
    withdraw_entry_button = tk.Button(
        canvas,
        text="Enter",
        command=lambda: (
            withdraw(wallet=wallet, category=get_category()),
            main_screen(
                previous_canvas=canvas,
                wallet=wallet))
    )

    withdraw_entry.bind("<KeyRelease>", add_commas)

    items = ["other", "snacks and drinks", "lunch bentos", "weekends"]
    list_items = tk.Variable(value=items)

    withdraw_category_label = tk.Label(canvas, text="Choose a category: ")
    withdraw_category_chooser = tk.Listbox(canvas, height=5, width=10, listvariable=list_items, selectmode=tk.SINGLE)


    def get_category():
        category_info = withdraw_category_chooser.curselection()
        category = withdraw_category_chooser.get(category_info)
        print(category)
        return category

    withdraw_entry.bind("<KeyRelease>", add_commas)

    # display widgets on screen
    canvas.create_window(200, 20, window=withdraw_label)
    canvas.create_window(200, 80, window=withdraw_entry)
    canvas.create_window(350, 80, window=withdraw_entry_button)
    canvas.create_window(100, 200, window=withdraw_category_label)
    canvas.create_window(250, 200, window=withdraw_category_chooser)

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
    wallet = Wallet(0, wallet_name, [], [])
    wallet_dicts = load_wallets()
    wallet_dicts.append(wallet.__dict__)
    with open("wallets.json", "w") as f:
        json.dump(wallet_dicts, f)
    return wallet


def deposit(wallet):

    amount = float(deposit_entry.get().replace(",", ""))
    wallet.deposit(amount)
    save_to_json(wallet)
    return wallet


def withdraw(wallet, category):

    amount = float(withdraw_entry.get().replace(",", ""))
    wallet.withdraw(amount, category)
    save_to_json(wallet)
    return wallet


welcome_screen()
root.mainloop()

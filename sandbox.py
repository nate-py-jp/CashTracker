import tkinter as tk

root = tk.Tk()

# Create a Listbox
listbox = tk.Listbox(root)
listbox.pack()

# Add some items to the Listbox
listbox.insert(1, "Item 1")
listbox.insert(2, "Item 2")
listbox.insert(3, "Item 3")


# Define a function to handle the selection event
def handle_selection(event):
    # Get the selected item
    selected_item = listbox.get(listbox.curselection())

    # Print the selected item
    print(selected_item)

# Bind the function to the selection event
listbox.bind("<<ListboxSelect>>", handle_selection)

root.mainloop()


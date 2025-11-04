#food_expiry_tracker_gui.py
# food_expiry_tracker_gui.py
# Author: Sophie Ashmore
# Description: Food Expiry Tracker app built using Python 
import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

# Data setup

food_list = []

def days_until_expiry(expiry_str):
    """Calculate how many days until expiry."""
    try:
        expiry = datetime.strptime(expiry_str, "%Y-%m-%d")
        today = datetime.today()
        return (expiry - today).days
    except ValueError:
        return None  # invalid date

def save_data():
    """Save current food list to a JSON file."""
    with open("fridge_data.json", "w") as f:
        json.dump(food_list, f)

def load_data():
    """Load existing food list from JSON file."""
    global food_list
    try:
        with open("fridge_data.json", "r") as f:
            food_list = json.load(f)
    except FileNotFoundError:
        food_list = []

def add_item():
    """Add new food item from user input."""
    name = entry_name.get()
    expiry = entry_expiry.get()

    if not name or not expiry:
        messagebox.showwarning("Error", "Please fill in all fields.")
        return

    days_left = days_until_expiry(expiry)
    if days_left is None:
        messagebox.showerror("Error", "Enter date in YYYY-MM-DD format.")
        return

    food_list.append({"name": name, "expiry": expiry})
    save_data()
    update_listbox()
    messagebox.showinfo("Added", f"{name} added successfully!")
    entry_name.delete(0, tk.END)
    entry_expiry.delete(0, tk.END)

def delete_item():
    """Delete selected food item."""
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Error", "Please select an item to delete.")
        return
    index = selection[0]
    del food_list[index]
    save_data()
    update_listbox()

def update_listbox():
    """Display all food items with colour coding."""
    listbox.delete(0, tk.END)
    for item in food_list:
        days = days_until_expiry(item["expiry"])
        if days is None:
            status = "Invalid date"
            colour = "grey"
        elif days < 0:
            status = "Expired"
            colour = "red"
        elif days <= 3:
            status = f"Expiring soon ({days} days left)"
            colour = "orange"
        else:
            status = f"Safe ({days} days left)"
            colour = "green"

        listbox.insert(tk.END, f"{item['name']} - {status}")
        listbox.itemconfig(tk.END, fg=colour)

# GUI setup

window = tk.Tk()
window.title("Food Expiry Tracker")
window.geometry("450x350")
window.configure(bg="white")

# Title
tk.Label(window, text="Welcome to Food Expiry Tracker",
         bg="white", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

# Input fields
tk.Label(window, text="Food Name", bg="white").grid(row=1, column=0, padx=10, pady=5)
entry_name = tk.Entry(window, width=25)
entry_name.grid(row=1, column=1, padx=10, pady=5)

tk.Label(window, text="Expiry Date (YYYY-MM-DD)", bg="white").grid(row=2, column=0, padx=10, pady=5)
entry_expiry = tk.Entry(window, width=25)
entry_expiry.grid(row=2, column=1, padx=10, pady=5)

# Buttons
add_button = tk.Button(window, text="Add Item", command=add_item,
                       bg="lightgreen", fg="black", width=15)
add_button.grid(row=3, column=0, pady=10)

delete_button = tk.Button(window, text="Delete Item", command=delete_item,
                          bg="lightcoral", fg="black", width=15)
delete_button.grid(row=3, column=1, pady=10)

# Listbox
listbox = tk.Listbox(window, width=50)
listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

load_data()
update_listbox()
window.mainloop()
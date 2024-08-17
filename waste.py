import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import datetime

class ElectronicItem:
    def __init__(self, name, serial_number, purchase_date, replacement_date, category):
        self.name = name
        self.serial_number = serial_number
        self.purchase_date = purchase_date
        self.replacement_date = replacement_date
        self.category = category
        self.status = "In use"
        self.history = [f"Item added on {datetime.date.today()}"]

class EWasteMonitoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Waste Monitoring System")
        self.items = []

        self.main_frame = tk.Frame(root, padx=20, pady=20, bg="#f0f8ff")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(self.main_frame, text="E-Waste Monitoring System", font=("Helvetica", 18, "bold"), bg="#f0f8ff", fg="#4682b4")
        self.title_label.grid(row=0, column=0, columnspan=8, pady=10)

        button_style = {'width': 18, 'bg': '#87cefa', 'fg': '#000000', 'relief': tk.RAISED, 'borderwidth': 2}
        self.add_button = tk.Button(self.main_frame, text="Add Item", command=self.add_item, **button_style)
        self.add_button.grid(row=1, column=0, padx=5, pady=10)

        self.monitor_button = tk.Button(self.main_frame, text="Monitor Items", command=self.display_items, **button_style)
        self.monitor_button.grid(row=1, column=1, padx=5, pady=10)

        self.edit_button = tk.Button(self.main_frame, text="Edit Item", command=self.edit_item, **button_style)
        self.edit_button.grid(row=1, column=2, padx=5, pady=10)

        self.replace_button = tk.Button(self.main_frame, text="Replace Item", command=self.replace_item, **button_style)
        self.replace_button.grid(row=1, column=3, padx=5, pady=10)

        self.delete_button = tk.Button(self.main_frame, text="Delete Item", command=self.delete_item, **button_style)
        self.delete_button.grid(row=1, column=4, padx=5, pady=10)

        self.clear_button = tk.Button(self.main_frame, text="Clear Table", command=self.clear_table, **button_style)
        self.clear_button.grid(row=1, column=5, padx=5, pady=10)

        self.category_button = tk.Button(self.main_frame, text="Category-Wise", command=self.display_category_wise, **button_style)
        self.category_button.grid(row=1, column=6, padx=5, pady=10)

        self.search_label = tk.Label(self.main_frame, text="Search by Name or Serial:", bg="#f0f8ff", fg="#4682b4")
        self.search_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')

        self.search_entry = tk.Entry(self.main_frame, width=20, font=("Helvetica", 12))
        self.search_entry.grid(row=2, column=1, padx=10, pady=10)

        self.search_button = tk.Button(self.main_frame, text="Search", command=self.search_item, **button_style)
        self.search_button.grid(row=2, column=2, padx=5, pady=10)

        self.tree = ttk.Treeview(self.main_frame, columns=('Name', 'Serial', 'Category', 'Purchase Date', 'Replacement Date', 'Status'), show='headings', style='Treeview')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Serial', text='Serial Number')
        self.tree.heading('Category', text='Category')
        self.tree.heading('Purchase Date', text='Purchase Date')
        self.tree.heading('Replacement Date', text='Replacement Date')
        self.tree.heading('Status', text='Status')

        self.tree.grid(row=3, column=0, columnspan=8, padx=10, pady=10)

        self.tree.column('Name', width=150)
        self.tree.column('Serial', width=100)
        self.tree.column('Category', width=120)
        self.tree.column('Purchase Date', width=150)
        self.tree.column('Replacement Date', width=150)
        self.tree.column('Status', width=100)

        # Treeview style
        style = ttk.Style()
        style.configure('Treeview', background='#f5f5f5', foreground='#000000', fieldbackground='#f5f5f5')
        style.configure('Treeview.Heading', background='#87cefa', foreground='#000000')

    def add_item(self):
        name = simpledialog.askstring("Input", "Enter item name (e.g., Laptop, Mobile Phone):")
        if not name:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        
        serial_number = simpledialog.askstring("Input", "Enter serial number:")
        category = simpledialog.askstring("Input", "Enter item category (e.g., Computers, Appliances):")
        
        while True:
            try:
                purchase_date = simpledialog.askstring("Input", "Enter purchase date (YYYY-MM-DD):")
                purchase_date = datetime.datetime.strptime(purchase_date, "%Y-%m-%d").date()
                replacement_date = simpledialog.askstring("Input", "Enter expected replacement date (YYYY-MM-DD):")
                replacement_date = datetime.datetime.strptime(replacement_date, "%Y-%m-%d").date()
                if replacement_date > purchase_date:
                    break
                else:
                    messagebox.showerror("Error", "Replacement date must be after the purchase date.")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Please enter the date in YYYY-MM-DD format.")

        item = ElectronicItem(name, serial_number, purchase_date, replacement_date, category)
        self.items.append(item)
        messagebox.showinfo("Success", f"Item '{name}' added successfully!")
        self.display_items()  
    def display_items(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in self.items:
            self.tree.insert('', 'end', values=(item.name, item.serial_number, item.category, item.purchase_date, item.replacement_date, item.status))

    def clear_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def edit_item(self):
        serial_number = simpledialog.askstring("Input", "Enter serial number of item to edit:")
        for item in self.items:
            if item.serial_number == serial_number:
                new_name = simpledialog.askstring("Input", "Enter new name:", initialvalue=item.name)
                new_purchase_date = simpledialog.askstring("Input", "Enter new purchase date (YYYY-MM-DD):", initialvalue=item.purchase_date)
                new_replacement_date = simpledialog.askstring("Input", "Enter new replacement date (YYYY-MM-DD):", initialvalue=item.replacement_date)
                
                item.name = new_name if new_name else item.name
                item.purchase_date = new_purchase_date if new_purchase_date else item.purchase_date
                item.replacement_date = new_replacement_date if new_replacement_date else item.replacement_date
                
                item.history.append(f"Item details edited on {datetime.date.today()}")
                messagebox.showinfo("Success", "Item details updated successfully!")
                self.display_items() 
                return
        messagebox.showerror("Error", "Item not found.")

    def delete_item(self):
        serial_number = simpledialog.askstring("Input", "Enter serial number of item to delete:")
        for i, item in enumerate(self.items):
            if item.serial_number == serial_number:
                del self.items[i]
                messagebox.showinfo("Success", f"Item '{item.name}' with serial '{serial_number}' has been deleted.")
                self.display_items()  
                return
        messagebox.showerror("Error", "Item not found.")

    def replace_item(self):
        serial_number = simpledialog.askstring("Input", "Enter serial number of item to replace:")
        for item in self.items:
            if item.serial_number == serial_number:
                new_replacement_date = simpledialog.askstring("Input", "Enter new replacement date (YYYY-MM-DD):")
                try:
                    new_replacement_date = datetime.datetime.strptime(new_replacement_date, "%Y-%m-%d").date()
                    if new_replacement_date > item.purchase_date:
                        item.replacement_date = new_replacement_date
                        item.status = "Replaced"
                        item.history.append(f"Item replaced on {datetime.date.today()}")
                        messagebox.showinfo("Success", f"Item '{item.name}' replaced successfully.")
                        self.display_items()  # Update the table after replacing an item
                        return
                    else:
                        messagebox.showerror("Error", "Replacement date must be after the purchase date.")
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format. Please enter the date in YYYY-MM-DD format.")
                return
        messagebox.showerror("Error", "Item not found.")

    def display_category_wise(self):
        category = simpledialog.askstring("Input", "Enter category to filter (e.g., Computers, Appliances):")
        if not category:
            messagebox.showerror("Error", "Category cannot be empty!")
            return
        
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in self.items:
            if item.category.lower() == category.lower():
                self.tree.insert('', 'end', values=(item.name, item.serial_number, item.category, item.purchase_date, item.replacement_date, item.status))

    def search_item(self):
        search_term = self.search_entry.get()
        if not search_term:
            messagebox.showerror("Error", "Search term cannot be empty!")
            return
        
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in self.items:
            if search_term.lower() in item.name.lower() or search_term.lower() in item.serial_number.lower():
                self.tree.insert('', 'end', values=(item.name, item.serial_number, item.category, item.purchase_date, item.replacement_date, item.status))

if __name__ == "__main__":
    root = tk.Tk()
    app = EWasteMonitoringApp(root)
    root.mainloop()

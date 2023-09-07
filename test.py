import tkinter as tk
from tkinter import ttk
from support import MyDB

class InventoryWidget(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.widgets = []
        self.db = MyDB()
        self.items = self.db.getStocks() 
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.update_items()
        self.update_scrollregion()

    def update_items(self):
        self.items = self.db.getStocks() 
        for widget in self.widgets:
            widget.destroy()
        self.widgets = []
        for item, quantity in self.items:
            row_frame = ttk.Frame(self.frame)
            label = ttk.Label(row_frame, text=f"{item}: {quantity}", width="80%")
            decrement_button = ttk.Button(row_frame, text="-", command=lambda: self.decrement_item(item), width="20%")

            label.pack(side="left")
            decrement_button.pack(side="left")
            row_frame.pack(fill="x")
            self.widgets.append(row_frame)

    def decrement_item(self, item):
        print(item[0])
        print(self.items)
        if item in self.items:
            print("ok")
            if item > 0 :   
                print("ok")
                newamount = self.db.getStock()[2] -1
                self.db.editStock(item, newamount)
                self.update_items()
                self.update_scrollregion()

    def update_scrollregion(self):
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

# Example usage:
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("300x300")

    items = {
        "Item 1": 5,
        "Item 2": 8,
        "Item 3": 3,
        "Item 4": 10,
        "Item 5": 2,
    }

    inventory_widget = InventoryWidget(root)
    inventory_widget.pack(fill="both", expand=True)

    root.mainloop()

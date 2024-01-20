import sqlite3
import sys
import os
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import socket
import threading

global state
state=False

class MyDB:
    def __init__(self, ui, db='testdb.db'):
        self.db = db
        self.ui = ui
        self.querie_db('''
            CREATE TABLE IF NOT EXISTS "Customers" (
                "ID"	INTEGER NOT NULL UNIQUE,
                "HouseID"	TEXT NOT NULL,
                "CardID"	TEXT,
                "Name"	TEXT NOT NULL,
                "DOB"	DATE,
                "Number"	TEXT NOT NULL,
                "CreditLimit"	INTEGER NOT NULL DEFAULT 0,
                "Balance"	INTEGER NOT NULL DEFAULT 0,
                "MPoints"	INTEGER DEFAULT 0,
                PRIMARY KEY("ID" AUTOINCREMENT));''')
        
        self.querie_db('''
            CREATE TABLE IF NOT EXISTS "Users" (
                "ID"	TEXT NOT NULL UNIQUE,
                "Name"	TEXT NOT NULL,
                "Privilege"	INTEGER NOT NULL,
                PRIMARY KEY("ID"));''')
        
        self.querie_db('''
        CREATE TABLE IF NOT EXISTS "Sales" (
            "ID" INTEGER NOT NULL UNIQUE,
            "UserID" INTEGER NOT NULL,
            "CustomerID" INTEGER NOT NULL,
            "Amount" INTEGER NOT NULL,
            "Timestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            "Receipt" TEXT,
            PRIMARY KEY("ID" AUTOINCREMENT),
            FOREIGN KEY("UserID") REFERENCES "Users"("ID"),
            FOREIGN KEY("CustomerID") REFERENCES "Customers"("ID"));''')

        self.querie_db('''
            CREATE TABLE IF NOT EXISTS "Purchases" (
                "ID"	INTEGER NOT NULL UNIQUE,
                "UserID"	INTEGER NOT NULL,
                "Amount"	INTEGER NOT NULL,
                "Description"	TEXT NOT NULL,
                PRIMARY KEY("ID" AUTOINCREMENT),
                FOREIGN KEY("UserID") REFERENCES "Users"("ID"));''')

        self.querie_db('''
            CREATE TABLE IF NOT EXISTS "Menu" (
                "ID"	INTEGER NOT NULL UNIQUE,
                "Item"	TEXT NOT NULL,
                "Price"	INTEGER NOT NULL,
                PRIMARY KEY("ID" AUTOINCREMENT));''')
        
    def querie_db(self, query):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute(query)
            reply = cursor.fetchall()
            conn.commit()
            conn.close()
            return reply
        except:
            pass
    
    # Customers
    def getCustomers(self):
        query = '''SELECT * FROM Customers'''
        return self.querie_db(query)
    
    def addCustomer(self, house_id, card_id, name, dob, number, credit_limit=0, balance=0, m_points=0):
        query = f'''SELECT * FROM CUSTOMERS WHERE Name Like "{name}" AND DOB = "{dob}" OR Number = "{number}"'''
        if not self.querie_db(query):
            query = f'''
                INSERT INTO Customers (HouseID, CardID, Name, DOB, Number, CreditLimit, Balance, MPoints)
                VALUES ('{house_id}', '{card_id}', '{name}', '{dob}', '{number}', '{credit_limit}', '{balance}', '{m_points}');
            '''
            if house_id and card_id and name and dob and number:
                self.querie_db(query)
    
    def editCustomer(self, customer_id, house_id=None, card_id=None, name=None, dob=None, number=None,
                    credit_limit=None, balance=None, m_points=None):
        # Define default values for each field
        default_house_id = "Guest"
        default_card_id = "None"
        default_name = "No Name"
        default_dob = "01-01-2001"
        default_number = ""
        default_credit_limit = 0
        default_balance = 0
        default_m_points = 0

        # Check each input and set to default if it's a string or None
        if house_id is None or not isinstance(house_id, str):
            house_id = default_house_id
        if card_id is None or not isinstance(card_id, str):
            card_id = default_card_id
        if name is None or not isinstance(name, str):
            name = default_name
        if dob is None or not isinstance(dob, str):
            dob = default_dob
        if number is None or not isinstance(number, str):
            number = default_number
        if credit_limit is None or not isinstance(credit_limit, (int, float)):
            credit_limit = default_credit_limit
        if balance is None or not isinstance(balance, (int, float)):
            balance = default_balance
        if m_points is None or not isinstance(m_points, int):
            m_points = default_m_points

        # Create a list to store the individual update statements
        update_statements = []

        # Add the updates to the update_statements list
        update_statements.append(f'HouseID = "{house_id}"')
        update_statements.append(f'CardID = "{card_id}"')
        update_statements.append(f'Name = "{name}"')
        update_statements.append(f'DOB = "{dob}"')
        update_statements.append(f'Number = "{number}"')
        update_statements.append(f'CreditLimit = {credit_limit}')
        update_statements.append(f'Balance = {balance}')
        update_statements.append(f'MPoints = {m_points}')

        # Start building the UPDATE query
        query = f'''UPDATE Customers SET {', '.join(update_statements)} WHERE ID = {customer_id};'''

        # Execute the query
        self.querie_db(query)

    def deleteCustomer(self, customer_id):
        query = f'''
            DELETE FROM Customers
            WHERE ID = {customer_id};
        '''
        self.querie_db(query)
    
    def getCustomer(self, card_id):
        query = f'''
            SELECT * FROM Customers
            WHERE CardID = '{card_id}';
        '''
        return self.querie_db(query)
    
    def getCustomerID(self, id):
        query = f'''
            SELECT * FROM Customers
            WHERE ID = '{id}';
        '''
        return self.querie_db(query)
    
    def topup(self, customerID, amount):
        query = f'SELECT Balance FROM Customers WHERE ID = {customerID}'
        balance = self.querie_db(query)

        if balance is not None:
            current_balance = balance[0][0]
            if amount is not None:
                # Calculate the new balance after top-up
                new_balance = current_balance + int(amount)
                query = f'UPDATE Customers SET Balance = {new_balance} WHERE ID = {customerID}'
                self.querie_db(query)
                return f"Successfully topped up {amount} to Customer ID {customerID}. New balance: {new_balance}"
            else:
                return
        else:
            return f"Customer ID {customerID} not found in the database."
    
    # Users
    def getUsers(self):
        query = '''SELECT * FROM Users'''
        return self.querie_db(query)

    def getUser(self, user_id):
        query = f'''
            SELECT * FROM Users
            WHERE ID = {user_id};
        '''
        return self.querie_db(query)
    
    def isUserAdmin(self, user_id):
        query = f'''
            SELECT Privilege FROM Users
            WHERE ID = '{user_id}';
        '''
        result = self.querie_db(query)
        
        # If the user is found and has privilege level 100, they are an admin
        if result and result[0][0] == 100:
            return True
        else:
            return False
    
    #Sales
    def addSale(self, user_id, customer_id, amount, receipt):
        query = f'''
            INSERT INTO Sales (UserID, CustomerID, Amount, Receipt)
            VALUES ("{user_id}", "{customer_id}", "{amount}", "{receipt}");
        '''
        self.querie_db(query)

    # Purchases
    def getPurchases(self):
        query = '''SELECT * FROM Purchases'''
        return self.querie_db(query)

    def addPurchase(self, user_id, amount, description):
        query = f'''
            INSERT INTO Purchases (UserID, Amount, Description)
            VALUES ('{user_id}', '{amount}', '{description}');
        '''
        self.querie_db(query)

    # Menu
    def get_unique_stock_items(self):
        query = 'SELECT DISTINCT Item FROM Menu'
        items = self.querie_db(query) 
        unique_items = [item[0] for item in items]
        return unique_items
    
    def getStocks(self):
        query = '''SELECT Item, Price FROM Menu'''
        return self.querie_db(query)

    def addStock(self, item, amount):  
        if self.getStock(item) != []:
            #self.editStock(item, int(self.getStock(item)[0][2]) + int(amount))
            self.editStock(item, int(amount))
            self.ui.stocks = self.getStocks()
            self.ui.values[item] = self.getStock(item)
            self.ui.top.destroy()
            python = sys.executable
            os.execl(python, python, *sys.argv)
        else:
            query = f'''
            INSERT INTO Menu (Item, Price)
            VALUES ("{item}", "{amount}");
            '''
            self.querie_db(query)
            self.ui.add_Last_Stock()
            self.ui.stocks = self.getStocks()
 
    def editStock(self, item, amount):
        query = f'''
            UPDATE Menu
            SET Price = "{amount}"
            WHERE Item = "{item}";
        '''
        self.querie_db(query)

    def deleteStock(self, stock_id):
        query = f'''
            DELETE FROM Menu
            WHERE ID = {stock_id};
        '''
        self.querie_db(query)

    def getStock(self, item):
        query = f'''
            SELECT * FROM Menu
            WHERE Item = "{item}";
        '''
        return self.querie_db(query)
       
class StockEntryForm:
    def __init__(self, user, ui):
        self.ui = ui
        self.parent = tk.Toplevel()
        self.parent.grab_set()
        self.db = MyDB(ui)
        self.user = user
        self.state = 1

    def start(self):
        self.parent.title("Add to Menu")
        self.parent.geometry("400x200")
        # Create a frame to contain the stock entry form
        self.frame = tk.Frame(self.parent)
        self.frame.pack()

        # Create a label and entry for item
        item_label = tk.Label(self.frame, text="Item:")
        item_label.pack()
        self.item_var = tk.StringVar()
        self.item_combobox = ttk.Combobox(self.frame, textvariable=self.item_var, state="normal")
        self.item_combobox.pack()

        # Create a label and entry for amount
        amount_label = tk.Label(self.frame, text="Sale Price:")
        amount_label.pack()
        self.amount_entry = tk.Entry(self.frame)
        self.amount_entry.pack()

        # Create a label and entry for price
        price_label = tk.Label(self.frame, text="Buy Price:")
        price_label.pack()
        self.price_entry = tk.Entry(self.frame)
        self.price_entry.pack()


        # Create a button to submit the form
        submit_button = tk.Button(self.frame, text="Submit", command=self.submit)
        submit_button.pack()

        # Populate the item dropdown with existing items
        stocks = self.db.get_unique_stock_items()
        self.item_combobox['values'] = stocks
    
    def submit(self):
        item = self.item_var.get()
        amount = self.amount_entry.get()
        price = self.price_entry.get()
        if not item or not amount or not price:
            messagebox.showerror("Error", "All fields are required.")
            return
        self.db.addStock(item, amount)
        self.db.addPurchase(self.user, amount, item)
        stocks = self.db.get_unique_stock_items()
        self.item_combobox['values'] = stocks
        self.item_var.set('')
        self.amount_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.parent.destroy()
        self.state = 0      

class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self['activebackground'] = "black"
        self['activeforeground'] = "pink"
        self['background'] = "black"
        self['font'] = ("forte", 14)
        self['compound'] = "left"
        self['bd'] = 0
        self['disabledforeground'] = "pink"
        self['foreground'] = "gold"
        self['highlightbackground'] = "black"
        self['highlightcolor'] = "pink"
        self['pady'] = "0"

    def on_enter(self, e):
        self['foreground'] = "red"

    def on_leave(self, e):
        self['foreground'] = "gold"

class Label(tk.Label):
    def __init__(self, master, **kw):
        tk.Label.__init__(self,master=master,**kw)        
        self['activebackground'] = "black"
        self['anchor'] = "w"
        self['background'] = "black"
        self['compound'] = "left"
        self['font'] = ("forte", 14)
        self['disabledforeground'] = "gold"
        self['foreground'] = "gold"
        self['highlightbackground'] = "black"
        self['highlightcolor'] = "pink"
                
class ScrolledFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.bind("<Configure>", self.on_canvas_configure)  # Bind to Configure event
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)

        self.update_scrollregion()

    def on_canvas_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def update_scrollregion(self):
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
   
class Log(tk.Frame):
    def __init__(self, parent, max_length=100, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.max_length = max_length
        self.text_list = []
        
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        
        self.canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.update_scrollregion()
    
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def update_scrollregion(self):
        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def append(self, text):
        if len(self.text_list) >= self.max_length:
            self.text_list.pop()  # Remove the oldest entry
        
        self.text_list.insert(0, text)  # Insert text at the beginning
        self.clear_frame()
        
        for i, entry in enumerate(self.text_list):
            label = ttk.Label(self.frame, text=entry, anchor="w", justify="left")
            label.grid(row=i, column=0, sticky="w")
        
        self.update_scrollregion()
    
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

class ScrolledTable(tk.Frame):
    def __init__(self, parent, ui, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.ui = ui
        self.db = MyDB(ui)  # Replace 'MyDB()' with your actual database class.

        # Create a Treeview widget to display the data
        self.tree = ttk.Treeview(self, columns=("ID", "House", "Name", "Balance"), show="headings")
        self.tree.heading("#1", text="ID")
        self.tree.heading("#2", text="House")
        self.tree.heading("#3", text="Name")
        self.tree.heading("#4", text="Balance")

        self.tree.column("#1", width=1)
        self.tree.column("#2", width=1)
        self.tree.column("#3", width=100)
        self.tree.column("#4", width=5)

        # Create a vertical scrollbar
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.update_treeview()
        self.tree.bind("<<TreeviewSelect>>", self.on_item_select)
        
    def clear_treeview(self):
        # Clear existing data in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

    def update_treeview(self):
        if self.ui.user:
            # Query data from the database
            data_from_db = self.db.querie_db('''SELECT ID, HouseID, Name, Balance from Customers''')

            self.clear_treeview()

            # Insert updated data into the Treeview
            for row in data_from_db:
                self.tree.insert("", "end", values=row)
        else:
            self.after(300, self.update_treeview)
        

    def on_item_select(self, event):
        if self.ui.user:
            # Get the selected item(s)
            selected_items = self.tree.selection()
            # Perform a task based on the selected item(s)
            if selected_items:
                for item in selected_items:
                    item_data = self.tree.item(item)
                    id = self.db.getCustomerID(item_data["values"][0])[0]
                    self.ui.NFCcustomer(id)
        else:
            self.after(300, self.on_item_select)

    def select_by_card_id(self, card_id):
        if self.ui.user:
            # Search for the row with the specified card ID
            for item in self.tree.get_children():
                item_data = self.tree.item(item)
                if item_data["values"][0] == card_id:
                    # Clear previous selections
                    self.tree.selection_remove(self.tree.selection())
                    
                    # Select the row
                    self.tree.selection_add(item)
                    
                    # Manually change the background color of the selected row
                    self.tree.item(item, {'tags': ('selected',)})
                    self.tree.item(item, {'values': item_data["values"], 'tags': ('selected',)})
                    
                    # Ensure the selected row is visible by scrolling to it
                    self.tree.see(item)
                    break
        else:
            self.after(300, self.select_by_card_id)        
             
class NFC():
    def __init__(self, ui):
        self.server_ip = self.getIPAddress()  # Laptop's IP address
        self.server_port = 2020  # Port used in NodeMCU code
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen()  # Listen for one connection
        self.db = MyDB(ui)
        self.ui = ui
        self.stop_event = threading.Event()
        
        self.t = threading.Thread(target=self.start_server)
        self.state = False
        
        self.known_nfc_data = self.db.getUsers()
        for i in range(len(self.known_nfc_data)):
            self.known_nfc_data[i] = self.known_nfc_data[i][0]
        
        self.customers = self.db.getCustomers() #["4b2efaa10289", "data1"]
        for i in range(len(self.customers)):
            self.customers[i] = self.customers[i][2] 
        self.start()
        
    def getIPAddress(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    
    def verify_nfc_card(self, data):
        self.known_nfc_data = self.db.getUsers()
        for i in range(len(self.known_nfc_data)):
            self.known_nfc_data[i] = self.known_nfc_data[i][0]
        if data in self.known_nfc_data:
            return True
        return False
    
    def get_customer(self, data):
        self.customers = self.db.getCustomers() #["4b2efaa10289", "data1"]
        for i in range(len(self.customers)):
            self.customers[i] = self.customers[i][2]
        if data in self.customers:
            return data
        return False

    def start(self):
        self.state = True
        self.t.start()
    
    def stop(self):
        self.stop_event.set()
        self.state = False
        
        
    def start_server(self):
        self.loggedin = False
        while self.state:
            try:
                self.client_socket, self.client_address = self.server_socket.accept()
                while self.state:
                    self.data = self.client_socket.recv(1024).decode('utf-8').strip()
                    if not self.data:
                        break 
                    if not self.loggedin and self.verify_nfc_card(self.data):
                        self.loggedin = True
                        self.ui.NFClogin(self.data, self.db.isUserAdmin(self.data)); 
                    elif self.loggedin and self.verify_nfc_card(self.data):
                        self.loggedin = False
                        self.ui.NFClogout()
                    elif self.data == "Fail":
                        self.ui.Logger("Reconnect NFC!", verbose = True)
                    elif self.data == "OK":
                        self.ui.Logger("NFC ready.", verbose = True)                        
                    elif self.loggedin and not (self.verify_nfc_card(self.data) or self.get_customer(self.data)):
                        self.ui.Logger("new card: "+str(self.data))
                        self.ui.NFCRegisterCard(self.data)                        
                    elif not self.loggedin and not self.verify_nfc_card(self.data):
                        self.ui.Logger("Unothorised!") 
                    elif self.loggedin and self.get_customer(self.data):
                        self.ui.Logger("Customer details: " + str(self.get_customer(self.data)))
                        self.ui.NFCcustomer(self.db.getCustomer(self.data)[0])
            except socket.error:
                self.ui.Logger("Error occurred while accepting connection. Retrying...")

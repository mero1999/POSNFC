import sqlite3
import tkinter as tk
import tkinter.ttk as ttk
import socket
import threading

class MyDB:
    def __init__(self, db='testdb.db'):
        self.db = db
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
                "ID"	INTEGER NOT NULL UNIQUE,
                "UserID"	INTEGER NOT NULL,
                "CustomerID"	INTEGER NOT NULL,
                "Amount"	INTEGER NOT NULL,
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
            CREATE TABLE IF NOT EXISTS "Stocks" (
                "ID"	INTEGER NOT NULL UNIQUE,
                "Item"	TEXT NOT NULL,
                "Amount"	INTEGER NOT NULL,
                PRIMARY KEY("ID" AUTOINCREMENT));''')
        
    def querie_db(self, query):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()
        cursor.execute(query)
        reply = cursor.fetchall()
        conn.commit()
        conn.close()
        return reply
    
    # Customers
    def getCustomers(self):
        query = '''SELECT * FROM Customers'''
        return self.querie_db(query)
    
    def addCustomer(self, house_id, card_id, name, dob, number, credit_limit=0, balance=0, m_points=0):
        query = f'''
            INSERT INTO Customers (HouseID, CardID, Name, DOB, Number, CreditLimit, Balance, MPoints)
            VALUES ('{house_id}', '{card_id}', '{name}', '{dob}', '{number}', {credit_limit}, {balance}, {m_points});
        '''
        self.querie_db(query)
    
    def editCustomer(self, customer_id, house_id, card_id, name, dob, number, credit_limit, balance, m_points):
        query = f'''
            UPDATE Customers
            SET HouseID = '{house_id}', CardID = '{card_id}', Name = '{name}', DOB = '{dob}', Number = '{number}',
                CreditLimit = {credit_limit}, Balance = {balance}, MPoints = {m_points}
            WHERE ID = {customer_id};
        '''
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
    
    # Users
    def getUsers(self):
        query = '''SELECT * FROM Users'''
        return self.querie_db(query)
    
    def addUser(self, name, privilege):
        query = f'''
            INSERT INTO Users (Name, Privilege)
            VALUES ('{name}', {privilege});
        '''
        self.querie_db(query)
    
    def editUser(self, user_id, name, privilege):
        query = f'''
            UPDATE Users
            SET Name = '{name}', Privilege = {privilege}
            WHERE ID = {user_id};
        '''
        self.querie_db(query)
    
    def deleteUser(self, user_id):
        query = f'''
            DELETE FROM Users
            WHERE ID = {user_id};
        '''
        self.querie_db(query)
    
    def getUser(self, user_id):
        query = f'''
            SELECT * FROM Users
            WHERE ID = {user_id};
        '''
        return self.querie_db(query)
     # Sales
    def getSales(self):
        query = '''SELECT * FROM Sales'''
        return self.querie_db(query)
    
    def addSale(self, user_id, customer_id, amount):
        query = f'''
            INSERT INTO Sales (UserID, CustomerID, Amount)
            VALUES ({user_id}, {customer_id}, {amount});
        '''
        self.querie_db(query)

    def editSale(self, sale_id, user_id, customer_id, amount):
        query = f'''
            UPDATE Sales
            SET UserID = {user_id}, CustomerID = {customer_id}, Amount = {amount}
            WHERE ID = {sale_id};
        '''
        self.querie_db(query)

    def deleteSale(self, sale_id):
        query = f'''
            DELETE FROM Sales
            WHERE ID = {sale_id};
        '''
        self.querie_db(query)

    def getSale(self, sale_id):
        query = f'''
            SELECT * FROM Sales
            WHERE ID = {sale_id};
        '''
        return self.querie_db(query)

    # Purchases
    def getPurchases(self):
        query = '''SELECT * FROM Purchases'''
        return self.querie_db(query)

    def addPurchase(self, user_id, amount, description):
        query = f'''
            INSERT INTO Purchases (UserID, Amount, Description)
            VALUES ({user_id}, {amount}, '{description}');
        '''
        self.querie_db(query)

    def editPurchase(self, purchase_id, user_id, amount, description):
        query = f'''
            UPDATE Purchases
            SET UserID = {user_id}, Amount = {amount}, Description = '{description}'
            WHERE ID = {purchase_id};
        '''
        self.querie_db(query)

    def deletePurchase(self, purchase_id):
        query = f'''
            DELETE FROM Purchases
            WHERE ID = {purchase_id};
        '''
        self.querie_db(query)

    def getPurchase(self, purchase_id):
        query = f'''
            SELECT * FROM Purchases
            WHERE ID = {purchase_id};
        '''
        return self.querie_db(query)

    # Stocks
    def getStocks(self):
        query = '''SELECT * FROM Stocks'''
        return self.querie_db(query)

    def addStock(self, item, amount):
        query = f'''
            INSERT INTO Stocks (Item, Amount)
            VALUES ('{item}', {amount});
        '''
        self.querie_db(query)

    def editStock(self, stock_id, item, amount):
        query = f'''
            UPDATE Stocks
            SET Item = '{item}', Amount = {amount}
            WHERE ID = {stock_id};
        '''
        self.querie_db(query)

    def deleteStock(self, stock_id):
        query = f'''
            DELETE FROM Stocks
            WHERE ID = {stock_id};
        '''
        self.querie_db(query)

    def getStock(self, stock_id):
        query = f'''
            SELECT * FROM Stocks
            WHERE ID = {stock_id};
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

class ScrolledFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
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
             
class NFC():
    def __init__(self, ui):
        self.server_ip = "192.168.1.105"  # Laptop's IP address
        self.server_port = 20920  # Port used in NodeMCU code
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen()  # Listen for one connection
        self.db = MyDB()
        self.ui = ui
        
        self.known_nfc_data = self.db.getUsers()
        for i in range(len(self.known_nfc_data)):
            self.known_nfc_data[i] = self.known_nfc_data[i][0]
        print(self.known_nfc_data)
        
        self.customers = self.db.getCustomers() #["4b2efaa10289", "data1"]
        for i in range(len(self.customers)):
            self.customers[i] = self.customers[i][2]
            
        self.start()

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
        threading.Thread(target=self.start_server).start()
        
    def start_server(self):
        self.loggedin = False
        while True:
            try:
                self.client_socket, self.client_address = self.server_socket.accept()
                while True:
                    self.data = self.client_socket.recv(1024).decode('utf-8').strip()
                    if not self.data:
                        break  # Exit the inner loop only if no more data is received
                    #print("data:", self.data)
                    if not self.loggedin and self.verify_nfc_card(self.data):
                        self.loggedin = True
                        print("admin: ",self.db.isUserAdmin(self.data))
                        self.ui.NFClogin(self.data, self.db.isUserAdmin(self.data));
                        print("Login successful!")
                        
                    elif self.loggedin and self.verify_nfc_card(self.data):
                        self.loggedin = False
                        self.ui.NFClogout();
                        print("logging out!")
                        
                    elif self.data == "Fail":
                        print("NFC Module failure, restart!")

                    elif self.data == "OK":
                        print("NFC Module ready. Waiting for a known card...")
                        
                    elif self.loggedin and not (self.verify_nfc_card(self.data) or self.get_customer(self.data)):
                        print("New card...")
                        self.ui.NFCRegisterCard(self.data)
                        
                    elif not self.loggedin and not self.verify_nfc_card(self.data):
                        print("Not logged in. Waiting for a login card...")

                    elif self.loggedin and self.get_customer(self.data):
                        print("Customer details: " + str(self.get_customer(self.data)))
                        self.ui.NFCcustomer(self.db.getCustomer(self.data)[0])
                        
            except socket.error:
                print("Error occurred while accepting connection. Retrying...") 
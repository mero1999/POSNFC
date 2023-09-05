#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

import sys
import socket
import sqlite3
import threading
import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import Calendar, DateEntry
from tkinter.constants import *


class MyDB:
    def __init__(self, db='testdb3.db'):
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
    
    def getCustomer(self, customer_id):
        query = f'''
            SELECT * FROM Customers
            WHERE ID = {customer_id};
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
    def __init__(self):
        self.server_ip = "192.168.1.105"  # Laptop's IP address
        self.server_port = 20920  # Port used in NodeMCU code
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen()  # Listen for one connection
        self.db = MyDB()
        
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
                        print("Login successful!")
                        
                    elif self.loggedin and self.verify_nfc_card(self.data):
                        self.loggedin = False
                        print("logging out!")
                        
                    elif self.data == "Fail":
                        print("NFC Module failure, restart!")

                    elif self.data == "OK":
                        print("NFC Module ready. Waiting for a known card...")
                        
                    elif self.loggedin and not (self.verify_nfc_card(self.data) or self.get_customer(self.data)):
                        print("Unknown NFC card. Waiting for a known card...")
                        #clear all Entries and show this data on CardEntry
                        ##try adding a method in ui to modify the entries and pass the ui(self) as an argument for NFC 
                        
                    elif not self.loggedin and not self.verify_nfc_card(self.data):
                        print("Unknown NFC card. Waiting for a known card...")

                    elif self.loggedin and self.get_customer(self.data):
                        print("Customer details: " + str(self.get_customer(self.data)))
                        
            except socket.error:
                print("Error occurred while accepting connection. Retrying...")        

class Toplevel1: 
    def __init__(self, top=None):
        self.B1 = 0
        self.B2 = 0
        self.B3 = 0
        self.B5 = 0
        self.B10 = 0
        self.B15 = 0

        self.sub1 = 0
        self.sub2 = 0
        self.sub3 = 0
        self.sub5 = 0
        self.sub10 = 0
        self.sub15 = 0

        self.total = 0
        
        self.UID = None
        self.Name = None
        self.House = None
        self.MP = None
        self.Number = None
        self.limit = None
        self.Balance = 50
        self.DOB = None
        self.Card = "ABDB"

        self.db = MyDB()
        self.users = self.db.getUsers()
        self.customers = self.db.getCustomers()
        self.stocks = self.db.getStocks()
        self.purchases = self.db.getPurchases()
        self.sales = self.db.getSales()
        
        print(self.users)
        print(self.customers)
        print(self.stocks)
        print(self.purchases)
        print(self.sales)

        self.nfc = NFC()
        
        top.geometry("1327x832+222+65")
        top.minsize(120, 1)
        top.maxsize(1924, 1061)
        top.resizable(1,  1)
        top.title("Toplevel 0")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.top = top

        self.Frame1 = tk.Frame(self.top)
        self.Frame1.place(relx=0.009, rely=0.013, relheight=0.954
                , relwidth=0.156)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="#d9d9d9")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")
        
        self.Frame2 = tk.Frame(self.Frame1)
        self.Frame2.place(relx=0.058, rely=0.053, relheight=0.841
                , relwidth=0.884)
        self.Frame2.configure(relief='groove')
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief="groove")
        self.Frame2.configure(background="#d9d9d9")
        self.Frame2.configure(highlightbackground="#d9d9d9")
        self.Frame2.configure(highlightcolor="black")
        
        self.z1 = tk.Button(self.Frame2)
        self.z1.place(relx=0.066, rely=0.046, height=74, width=137)
        self.z1.configure(activebackground="beige")
        self.z1.configure(activeforeground="black")
        self.z1.configure(background="#d9d9d9")
        self.z1.configure(command=self.Za2ateet1)
        self.z1.configure(compound='left')
        self.z1.configure(disabledforeground="#a3a3a3")
        self.z1.configure(foreground="#000000")
        self.z1.configure(highlightbackground="#d9d9d9")
        self.z1.configure(highlightcolor="black")
        self.z1.configure(pady="0")
        self.z1.configure(text='''1 Za2toot''')
        
        self.z2 = tk.Button(self.Frame2)
        self.z2.place(relx=0.066, rely=0.205, height=74, width=137)
        self.z2.configure(activebackground="beige")
        self.z2.configure(activeforeground="black")
        self.z2.configure(background="#d9d9d9")
        self.z2.configure(command=self.Za2ateet2)
        self.z2.configure(compound='left')
        self.z2.configure(disabledforeground="#a3a3a3")
        self.z2.configure(foreground="#000000")
        self.z2.configure(highlightbackground="#d9d9d9")
        self.z2.configure(highlightcolor="black")
        self.z2.configure(pady="0")
        self.z2.configure(text='''2 Za2toot''')
        
        self.z3 = tk.Button(self.Frame2)
        self.z3.place(relx=0.066, rely=0.362, height=74, width=137)
        self.z3.configure(activebackground="beige")
        self.z3.configure(activeforeground="black")
        self.z3.configure(background="#d9d9d9")
        self.z3.configure(command=self.Za2ateet3)
        self.z3.configure(compound='left')
        self.z3.configure(disabledforeground="#a3a3a3")
        self.z3.configure(foreground="#000000")
        self.z3.configure(highlightbackground="#d9d9d9")
        self.z3.configure(highlightcolor="black")
        self.z3.configure(pady="0")
        self.z3.configure(text='''3 Za2toot''')
        
        self.z5 = tk.Button(self.Frame2)
        self.z5.place(relx=0.066, rely=0.519, height=74, width=137)
        self.z5.configure(activebackground="beige")
        self.z5.configure(activeforeground="black")
        self.z5.configure(background="#d9d9d9")
        self.z5.configure(command=self.Za2ateet5)
        self.z5.configure(compound='left')
        self.z5.configure(cursor="fleur")
        self.z5.configure(disabledforeground="#a3a3a3")
        self.z5.configure(foreground="#000000")
        self.z5.configure(highlightbackground="#d9d9d9")
        self.z5.configure(highlightcolor="black")
        self.z5.configure(pady="0")
        self.z5.configure(text='''5 Za2toot''')
        
        self.z10 = tk.Button(self.Frame2)
        self.z10.place(relx=0.066, rely=0.677, height=74, width=137)
        self.z10.configure(activebackground="beige")
        self.z10.configure(activeforeground="black")
        self.z10.configure(background="#d9d9d9")
        self.z10.configure(command=self.Za2ateet10)
        self.z10.configure(compound='left')
        self.z10.configure(disabledforeground="#a3a3a3")
        self.z10.configure(foreground="#000000")
        self.z10.configure(highlightbackground="#d9d9d9")
        self.z10.configure(highlightcolor="black")
        self.z10.configure(pady="0")
        self.z10.configure(text='''10 Za2toot''')
        
        self.z15 = tk.Button(self.Frame2)
        self.z15.place(relx=0.066, rely=0.835, height=74
                , width=137)
        self.z15.configure(activebackground="beige")
        self.z15.configure(activeforeground="black")
        self.z15.configure(background="#d9d9d9")
        self.z15.configure(command=self.Za2ateet15)
        self.z15.configure(compound='left')
        self.z15.configure(disabledforeground="#a3a3a3")
        self.z15.configure(foreground="#000000")
        self.z15.configure(highlightbackground="#d9d9d9")
        self.z15.configure(highlightcolor="black")
        self.z15.configure(pady="0")
        self.z15.configure(text='''15 Za2toot''')
        
        self.BuyButton = tk.Button(self.Frame1)
        self.BuyButton.place(relx=0.058, rely=0.901, height=64, width=157)
        self.BuyButton.configure(activebackground="beige")
        self.BuyButton.configure(activeforeground="black")
        self.BuyButton.configure(background="#d9d9d9")
        self.BuyButton.configure(command=self.BUY)
        self.BuyButton.configure(compound='left')
        self.BuyButton.configure(disabledforeground="#a3a3a3")
        self.BuyButton.configure(foreground="#000000")
        self.BuyButton.configure(highlightbackground="#d9d9d9")
        self.BuyButton.configure(highlightcolor="black")
        self.BuyButton.configure(pady="0")
        self.BuyButton.configure(text='''Buy''')
        
        self.ItemsLabel = tk.Label(self.Frame1)
        self.ItemsLabel.place(relx=0.401, rely=0.013, height=23, width=40)
        self.ItemsLabel.configure(activebackground="#f9f9f9")
        self.ItemsLabel.configure(anchor='w')
        self.ItemsLabel.configure(background="#d9d9d9")
        self.ItemsLabel.configure(compound='left')
        self.ItemsLabel.configure(disabledforeground="#a3a3a3")
        self.ItemsLabel.configure(foreground="#000000")
        self.ItemsLabel.configure(highlightbackground="#d9d9d9")
        self.ItemsLabel.configure(highlightcolor="black")
        self.ItemsLabel.configure(text='''Items''')
        
        self.CartFrame = tk.Frame(self.top)
        self.CartFrame.place(relx=0.169, rely=0.013, relheight=0.954
                , relwidth=0.126)
        self.CartFrame.configure(relief='groove')
        self.CartFrame.configure(borderwidth="2")
        self.CartFrame.configure(relief="groove")
        self.CartFrame.configure(background="#d9d9d9")
        self.CartFrame.configure(highlightbackground="#d9d9d9")
        self.CartFrame.configure(highlightcolor="black")
        
        self.SubtotalFrame = tk.Frame(self.CartFrame)
        self.SubtotalFrame.place(relx=0.06, rely=0.053, relheight=0.841, relwidth=0.886)
        self.SubtotalFrame.configure(relief='groove')
        self.SubtotalFrame.configure(borderwidth="2")
        self.SubtotalFrame.configure(relief="groove")
        self.SubtotalFrame.configure(background="#d9d9d9")
        self.SubtotalFrame.configure(highlightbackground="#d9d9d9")
        self.SubtotalFrame.configure(highlightcolor="black")
        
        self.Z1AmountLabel = tk.Label(self.SubtotalFrame)
        self.Z1AmountLabel.place(relx=0.081, rely=0.079, height=22, width=40)
        self.Z1AmountLabel.configure(anchor='w')
        self.Z1AmountLabel.configure(background="#d9d9d9")
        self.Z1AmountLabel.configure(compound='left')
        self.Z1AmountLabel.configure(disabledforeground="#a3a3a3")
        self.Z1AmountLabel.configure(foreground="#000000")
        self.Z1AmountLabel.configure(text='''X   0''')   
        
        self.Z2AmountLabel = tk.Label(self.SubtotalFrame)
        self.Z2AmountLabel.place(relx=0.081, rely=0.237, height=22, width=40)
        self.Z2AmountLabel.configure(activebackground="#f9f9f9")
        self.Z2AmountLabel.configure(anchor='w')
        self.Z2AmountLabel.configure(background="#d9d9d9")
        self.Z2AmountLabel.configure(compound='left')
        self.Z2AmountLabel.configure(disabledforeground="#a3a3a3")
        self.Z2AmountLabel.configure(foreground="#000000")
        self.Z2AmountLabel.configure(highlightbackground="#d9d9d9")
        self.Z2AmountLabel.configure(highlightcolor="black")
        self.Z2AmountLabel.configure(text='''X   0''')
        
        self.Z3AmountLabel = tk.Label(self.SubtotalFrame)
        self.Z3AmountLabel.place(relx=0.081, rely=0.394, height=22, width=40)
        self.Z3AmountLabel.configure(activebackground="#f9f9f9")
        self.Z3AmountLabel.configure(anchor='w')
        self.Z3AmountLabel.configure(background="#d9d9d9")
        self.Z3AmountLabel.configure(compound='left')
        self.Z3AmountLabel.configure(disabledforeground="#a3a3a3")
        self.Z3AmountLabel.configure(foreground="#000000")
        self.Z3AmountLabel.configure(highlightbackground="#d9d9d9")
        self.Z3AmountLabel.configure(highlightcolor="black")
        self.Z3AmountLabel.configure(text='''X   0''')
        
        self.Z5AmountLabel = tk.Label(self.SubtotalFrame)
        self.Z5AmountLabel.place(relx=0.081, rely=0.551, height=22, width=40)
        self.Z5AmountLabel.configure(activebackground="#f9f9f9")
        self.Z5AmountLabel.configure(anchor='w')
        self.Z5AmountLabel.configure(background="#d9d9d9")
        self.Z5AmountLabel.configure(compound='left')
        self.Z5AmountLabel.configure(disabledforeground="#a3a3a3")
        self.Z5AmountLabel.configure(foreground="#000000")
        self.Z5AmountLabel.configure(highlightbackground="#d9d9d9")
        self.Z5AmountLabel.configure(highlightcolor="black")
        self.Z5AmountLabel.configure(text='''X   0''')
        
        self.Z10AmountLabel = tk.Label(self.SubtotalFrame)
        self.Z10AmountLabel.place(relx=0.081, rely=0.71, height=22, width=40)
        self.Z10AmountLabel.configure(activebackground="#f9f9f9")
        self.Z10AmountLabel.configure(anchor='w')
        self.Z10AmountLabel.configure(background="#d9d9d9")
        self.Z10AmountLabel.configure(compound='left')
        self.Z10AmountLabel.configure(disabledforeground="#a3a3a3")
        self.Z10AmountLabel.configure(foreground="#000000")
        self.Z10AmountLabel.configure(highlightbackground="#d9d9d9")
        self.Z10AmountLabel.configure(highlightcolor="black")
        self.Z10AmountLabel.configure(text='''X   0''')
        
        self.Z15AmountLabel = tk.Label(self.SubtotalFrame)
        self.Z15AmountLabel.place(relx=0.081, rely=0.865, height=23, width=40)
        self.Z15AmountLabel.configure(activebackground="#f9f9f9")
        self.Z15AmountLabel.configure(anchor='w')
        self.Z15AmountLabel.configure(background="#d9d9d9")
        self.Z15AmountLabel.configure(compound='left')
        self.Z15AmountLabel.configure(disabledforeground="#a3a3a3")
        self.Z15AmountLabel.configure(foreground="#000000")
        self.Z15AmountLabel.configure(highlightbackground="#d9d9d9")
        self.Z15AmountLabel.configure(highlightcolor="black")
        self.Z15AmountLabel.configure(text='''X   0''')

        self.Z1SubtotalLabel = tk.Label(self.SubtotalFrame)
        self.Z1SubtotalLabel.place(relx=0.081, rely=0.109, height=23, width=87)
        self.Z1SubtotalLabel.configure(anchor='w')
        self.Z1SubtotalLabel.configure(background="#d9d9d9")
        self.Z1SubtotalLabel.configure(compound='left')
        self.Z1SubtotalLabel.configure(disabledforeground="#a3a3a3")
        self.Z1SubtotalLabel.configure(foreground="#000000")
        self.Z1SubtotalLabel.configure(text='''Sub-total: 0''')
        
        self.Z2SubtotalLabel = tk.Label(self.SubtotalFrame)
        self.Z2SubtotalLabel.place(relx=0.081, rely=0.268, height=22, width=87)
        self.Z2SubtotalLabel.configure(activebackground="#f9f9f9")
        self.Z2SubtotalLabel.configure(anchor='w')
        self.Z2SubtotalLabel.configure(background="#d9d9d9")
        self.Z2SubtotalLabel.configure(compound='left')
        self.Z2SubtotalLabel.configure(disabledforeground="#a3a3a3")
        self.Z2SubtotalLabel.configure(foreground="#000000")
        self.Z2SubtotalLabel.configure(highlightbackground="#d9d9d9")
        self.Z2SubtotalLabel.configure(highlightcolor="black")
        self.Z2SubtotalLabel.configure(text='''Sub-total: 0''')
        
        self.Z3SubtotalLabel = tk.Label(self.SubtotalFrame)
        self.Z3SubtotalLabel.place(relx=0.081, rely=0.425, height=22, width=87)
        self.Z3SubtotalLabel.configure(activebackground="#f9f9f9")
        self.Z3SubtotalLabel.configure(anchor='w')
        self.Z3SubtotalLabel.configure(background="#d9d9d9")
        self.Z3SubtotalLabel.configure(compound='left')
        self.Z3SubtotalLabel.configure(disabledforeground="#a3a3a3")
        self.Z3SubtotalLabel.configure(foreground="#000000")
        self.Z3SubtotalLabel.configure(highlightbackground="#d9d9d9")
        self.Z3SubtotalLabel.configure(highlightcolor="black")
        self.Z3SubtotalLabel.configure(text='''Sub-total: 0''')
        
        self.Z5SubtotalLabel = tk.Label(self.SubtotalFrame)
        self.Z5SubtotalLabel.place(relx=0.081, rely=0.582, height=22, width=87)
        self.Z5SubtotalLabel.configure(activebackground="#f9f9f9")
        self.Z5SubtotalLabel.configure(anchor='w')
        self.Z5SubtotalLabel.configure(background="#d9d9d9")
        self.Z5SubtotalLabel.configure(compound='left')
        self.Z5SubtotalLabel.configure(disabledforeground="#a3a3a3")
        self.Z5SubtotalLabel.configure(foreground="#000000")
        self.Z5SubtotalLabel.configure(highlightbackground="#d9d9d9")
        self.Z5SubtotalLabel.configure(highlightcolor="black")
        self.Z5SubtotalLabel.configure(text='''Sub-total: 0''')
        
        self.Z10SubtotalLabel = tk.Label(self.SubtotalFrame)
        self.Z10SubtotalLabel.place(relx=0.081, rely=0.74, height=22, width=87)
        self.Z10SubtotalLabel.configure(activebackground="#f9f9f9")
        self.Z10SubtotalLabel.configure(anchor='w')
        self.Z10SubtotalLabel.configure(background="#d9d9d9")
        self.Z10SubtotalLabel.configure(compound='left')
        self.Z10SubtotalLabel.configure(disabledforeground="#a3a3a3")
        self.Z10SubtotalLabel.configure(foreground="#000000")
        self.Z10SubtotalLabel.configure(highlightbackground="#d9d9d9")
        self.Z10SubtotalLabel.configure(highlightcolor="black")
        self.Z10SubtotalLabel.configure(text='''Sub-total: 0''')
        
        self.Z15SubtotalLabel = tk.Label(self.SubtotalFrame)
        self.Z15SubtotalLabel.place(relx=0.081, rely=0.898, height=22, width=87)
        self.Z15SubtotalLabel.configure(activebackground="#f9f9f9")
        self.Z15SubtotalLabel.configure(anchor='w')
        self.Z15SubtotalLabel.configure(background="#d9d9d9")
        self.Z15SubtotalLabel.configure(compound='left')
        self.Z15SubtotalLabel.configure(disabledforeground="#a3a3a3")
        self.Z15SubtotalLabel.configure(foreground="#000000")
        self.Z15SubtotalLabel.configure(highlightbackground="#d9d9d9")
        self.Z15SubtotalLabel.configure(highlightcolor="black")
        self.Z15SubtotalLabel.configure(text='''Sub-total: 0''')
        
        self.Z1nButton = tk.Button(self.SubtotalFrame)
        self.Z1nButton.place(relx=0.797, rely=0.079, height=24, width=17)
        self.Z1nButton.configure(activebackground="beige")
        self.Z1nButton.configure(activeforeground="black")
        self.Z1nButton.configure(background="#d9d9d9")
        self.Z1nButton.configure(command=self.Za2ateet1n)
        self.Z1nButton.configure(compound='left')
        self.Z1nButton.configure(disabledforeground="#a3a3a3")
        self.Z1nButton.configure(foreground="#000000")
        self.Z1nButton.configure(highlightbackground="#d9d9d9")
        self.Z1nButton.configure(highlightcolor="black")
        self.Z1nButton.configure(pady="0")
        self.Z1nButton.configure(text='''-''')
        
        self.Z2nButton = tk.Button(self.SubtotalFrame)
        self.Z2nButton.place(relx=0.797, rely=0.237, height=24, width=17)
        self.Z2nButton.configure(activebackground="beige")
        self.Z2nButton.configure(activeforeground="black")
        self.Z2nButton.configure(background="#d9d9d9")
        self.Z2nButton.configure(command=self.Za2ateet2n)
        self.Z2nButton.configure(compound='left')
        self.Z2nButton.configure(disabledforeground="#a3a3a3")
        self.Z2nButton.configure(foreground="#000000")
        self.Z2nButton.configure(highlightbackground="#d9d9d9")
        self.Z2nButton.configure(highlightcolor="black")
        self.Z2nButton.configure(pady="0")
        self.Z2nButton.configure(text='''-''')
        
        self.Z3nButton = tk.Button(self.SubtotalFrame)
        self.Z3nButton.place(relx=0.797, rely=0.394, height=24, width=17)
        self.Z3nButton.configure(activebackground="beige")
        self.Z3nButton.configure(activeforeground="black")
        self.Z3nButton.configure(background="#d9d9d9")
        self.Z3nButton.configure(command=self.Za2ateet3n)
        self.Z3nButton.configure(compound='left')
        self.Z3nButton.configure(disabledforeground="#a3a3a3")
        self.Z3nButton.configure(foreground="#000000")
        self.Z3nButton.configure(highlightbackground="#d9d9d9")
        self.Z3nButton.configure(highlightcolor="black")
        self.Z3nButton.configure(pady="0")
        self.Z3nButton.configure(text='''-''')
        
        self.Z5nButton = tk.Button(self.SubtotalFrame)
        self.Z5nButton.place(relx=0.797, rely=0.551, height=24, width=17)
        self.Z5nButton.configure(activebackground="beige")
        self.Z5nButton.configure(activeforeground="black")
        self.Z5nButton.configure(background="#d9d9d9")
        self.Z5nButton.configure(command=self.Za2ateet5n)
        self.Z5nButton.configure(compound='left')
        self.Z5nButton.configure(disabledforeground="#a3a3a3")
        self.Z5nButton.configure(foreground="#000000")
        self.Z5nButton.configure(highlightbackground="#d9d9d9")
        self.Z5nButton.configure(highlightcolor="black")
        self.Z5nButton.configure(pady="0")
        self.Z5nButton.configure(text='''-''')
        
        self.Z10nButton = tk.Button(self.SubtotalFrame)
        self.Z10nButton.place(relx=0.797, rely=0.71, height=24, width=17)
        self.Z10nButton.configure(activebackground="beige")
        self.Z10nButton.configure(activeforeground="black")
        self.Z10nButton.configure(background="#d9d9d9")
        self.Z10nButton.configure(command=self.Za2ateet10n)
        self.Z10nButton.configure(compound='left')
        self.Z10nButton.configure(disabledforeground="#a3a3a3")
        self.Z10nButton.configure(foreground="#000000")
        self.Z10nButton.configure(highlightbackground="#d9d9d9")
        self.Z10nButton.configure(highlightcolor="black")
        self.Z10nButton.configure(pady="0")
        self.Z10nButton.configure(text='''-''')
        
        self.Z15nButton = tk.Button(self.SubtotalFrame)
        self.Z15nButton.place(relx=0.797, rely=0.865, height=24, width=17)
        self.Z15nButton.configure(activebackground="beige")
        self.Z15nButton.configure(activeforeground="black")
        self.Z15nButton.configure(background="#d9d9d9")
        self.Z15nButton.configure(command=self.Za2ateet15n)
        self.Z15nButton.configure(compound='left')
        self.Z15nButton.configure(disabledforeground="#a3a3a3")
        self.Z15nButton.configure(foreground="#000000")
        self.Z15nButton.configure(highlightbackground="#d9d9d9")
        self.Z15nButton.configure(highlightcolor="black")
        self.Z15nButton.configure(pady="0")
        self.Z15nButton.configure(text='''-''')
        
        self.TotalLabel = tk.Label(self.CartFrame)
        self.TotalLabel.place(relx=0.072, rely=0.914, height=22, width=111)
        self.TotalLabel.configure(activebackground="#f9f9f9")
        self.TotalLabel.configure(anchor='w')
        self.TotalLabel.configure(background="#d9d9d9")
        self.TotalLabel.configure(compound='left')
        self.TotalLabel.configure(disabledforeground="#a3a3a3")
        self.TotalLabel.configure(foreground="#000000")
        self.TotalLabel.configure(highlightbackground="#d9d9d9")
        self.TotalLabel.configure(highlightcolor="black")
        self.TotalLabel.configure(text='''Total: 0''')
        
        self.PayButton = tk.Button(self.CartFrame)
        self.PayButton.place(relx=0.072, rely=0.953, height=24, width=47)
        self.PayButton.configure(activebackground="beige")
        self.PayButton.configure(activeforeground="black")
        self.PayButton.configure(background="#d9d9d9")
        self.PayButton.configure(command=self.Pay)
        self.PayButton.configure(compound='left')
        self.PayButton.configure(disabledforeground="#a3a3a3")
        self.PayButton.configure(foreground="#000000")
        self.PayButton.configure(highlightbackground="#d9d9d9")
        self.PayButton.configure(highlightcolor="black")
        self.PayButton.configure(pady="0")
        self.PayButton.configure(text='''Pay''')
        
        self.ResetButton = tk.Button(self.CartFrame)
        self.ResetButton.place(relx=0.497, rely=0.953, height=24, width=47)
        self.ResetButton.configure(activebackground="beige")
        self.ResetButton.configure(activeforeground="black")
        self.ResetButton.configure(background="#d9d9d9")
        self.ResetButton.configure(command=self.Reset)
        self.ResetButton.configure(compound='left')
        self.ResetButton.configure(disabledforeground="#a3a3a3")
        self.ResetButton.configure(foreground="#000000")
        self.ResetButton.configure(highlightbackground="#d9d9d9")
        self.ResetButton.configure(highlightcolor="black")
        self.ResetButton.configure(pady="0")
        self.ResetButton.configure(text='''Reset''')
        
        self.CartLabel = tk.Label(self.CartFrame)
        self.CartLabel.place(relx=0.383, rely=0.013, height=23, width=40)
        self.CartLabel.configure(activebackground="#f9f9f9")
        self.CartLabel.configure(anchor='w')
        self.CartLabel.configure(background="#d9d9d9")
        self.CartLabel.configure(compound='left')
        self.CartLabel.configure(disabledforeground="#a3a3a3")
        self.CartLabel.configure(foreground="#000000")
        self.CartLabel.configure(highlightbackground="#d9d9d9")
        self.CartLabel.configure(highlightcolor="black")
        self.CartLabel.configure(text='''Cart''')
        
        self.CustomerFrame = tk.Frame(self.top)
        self.CustomerFrame.place(relx=0.303, rely=0.013, relheight=0.954, relwidth=0.29)
        self.CustomerFrame.configure(relief='groove')
        self.CustomerFrame.configure(borderwidth="2")
        self.CustomerFrame.configure(relief="groove")
        self.CustomerFrame.configure(background="#d9d9d9")
        self.CustomerFrame.configure(highlightbackground="#d9d9d9")
        self.CustomerFrame.configure(highlightcolor="black")
        
        self.CustomerDetailsFrame = tk.Frame(self.CustomerFrame)
        self.CustomerDetailsFrame.place(relx=0.031, rely=0.053, relheight=0.325, relwidth=0.935)
        self.CustomerDetailsFrame.configure(relief='groove')
        self.CustomerDetailsFrame.configure(borderwidth="2")
        self.CustomerDetailsFrame.configure(relief="groove")
        self.CustomerDetailsFrame.configure(background="#d9d9d9")
        self.CustomerDetailsFrame.configure(highlightbackground="#d9d9d9")
        self.CustomerDetailsFrame.configure(highlightcolor="black")
        
        self.NameLabel = tk.Label(self.CustomerDetailsFrame)
        self.NameLabel.place(relx=0.072, rely=0.062, height=45, width=52)
        self.NameLabel.configure(activebackground="#f9f9f9")
        self.NameLabel.configure(anchor='w')
        self.NameLabel.configure(background="#d9d9d9")
        self.NameLabel.configure(compound='left')
        self.NameLabel.configure(disabledforeground="#a3a3a3")
        self.NameLabel.configure(foreground="#000000")
        self.NameLabel.configure(highlightbackground="#d9d9d9")
        self.NameLabel.configure(highlightcolor="black")
        self.NameLabel.configure(text='''Name:''')
        
        self.HouseLabel = tk.Label(self.CustomerDetailsFrame)
        self.HouseLabel.place(relx=0.067, rely=0.194, height=33, width=52)
        self.HouseLabel.configure(activebackground="#f9f9f9")
        self.HouseLabel.configure(anchor='w')
        self.HouseLabel.configure(background="#d9d9d9")
        self.HouseLabel.configure(compound='left')
        self.HouseLabel.configure(disabledforeground="#a3a3a3")
        self.HouseLabel.configure(foreground="#000000")
        self.HouseLabel.configure(highlightbackground="#d9d9d9")
        self.HouseLabel.configure(highlightcolor="black")
        self.HouseLabel.configure(text='''House:''')
        
        self.MPLabel = tk.Label(self.CustomerDetailsFrame)
        self.MPLabel.place(relx=0.017, rely=0.295, height=34, width=75)
        self.MPLabel.configure(activebackground="#f9f9f9")
        self.MPLabel.configure(anchor='w')
        self.MPLabel.configure(background="#d9d9d9")
        self.MPLabel.configure(compound='left')
        self.MPLabel.configure(disabledforeground="#a3a3a3")
        self.MPLabel.configure(foreground="#000000")
        self.MPLabel.configure(highlightbackground="#d9d9d9")
        self.MPLabel.configure(highlightcolor="black")
        self.MPLabel.configure(text='''M-Points:''')
        
        self.NumberLabel = tk.Label(self.CustomerDetailsFrame)
        self.NumberLabel.place(relx=0.033, rely=0.395, height=34, width=64)
        self.NumberLabel.configure(activebackground="#f9f9f9")
        self.NumberLabel.configure(anchor='w')
        self.NumberLabel.configure(background="#d9d9d9")
        self.NumberLabel.configure(compound='left')
        self.NumberLabel.configure(disabledforeground="#a3a3a3")
        self.NumberLabel.configure(foreground="#000000")
        self.NumberLabel.configure(highlightbackground="#d9d9d9")
        self.NumberLabel.configure(highlightcolor="black")
        self.NumberLabel.configure(text='''Number:''')
        
        self.LimitLabel = tk.Label(self.CustomerDetailsFrame)
        self.LimitLabel.place(relx=0.042, rely=0.496, height=35, width=64)
        self.LimitLabel.configure(activebackground="#f9f9f9")
        self.LimitLabel.configure(anchor='w')
        self.LimitLabel.configure(background="#d9d9d9")
        self.LimitLabel.configure(compound='left')
        self.LimitLabel.configure(disabledforeground="#a3a3a3")
        self.LimitLabel.configure(foreground="#000000")
        self.LimitLabel.configure(highlightbackground="#d9d9d9")
        self.LimitLabel.configure(highlightcolor="black")
        self.LimitLabel.configure(text='''N-Limit:''')
        
        self.BalanceLabel = tk.Label(self.CustomerDetailsFrame)
        self.BalanceLabel.place(relx=0.042, rely=0.636, height=22, width=64)
        self.BalanceLabel.configure(activebackground="#f9f9f9")
        self.BalanceLabel.configure(anchor='w')
        self.BalanceLabel.configure(background="#d9d9d9")
        self.BalanceLabel.configure(compound='left')
        self.BalanceLabel.configure(disabledforeground="#a3a3a3")
        self.BalanceLabel.configure(foreground="#000000")
        self.BalanceLabel.configure(highlightbackground="#d9d9d9")
        self.BalanceLabel.configure(highlightcolor="black")
        self.BalanceLabel.configure(text='''Balance:''')

        self.DOBLabel = tk.Label(self.CustomerDetailsFrame)
        self.DOBLabel.place(relx=0.078, rely=0.744, height=22, width=52)
        self.DOBLabel.configure(activebackground="#f9f9f9")
        self.DOBLabel.configure(anchor='w')
        self.DOBLabel.configure(background="#d9d9d9")
        self.DOBLabel.configure(compound='left')
        self.DOBLabel.configure(disabledforeground="#a3a3a3")
        self.DOBLabel.configure(foreground="#000000")
        self.DOBLabel.configure(highlightbackground="#d9d9d9")
        self.DOBLabel.configure(highlightcolor="black")
        self.DOBLabel.configure(text='''D.O.B:''')

        self.CardLabel = tk.Label(self.CustomerDetailsFrame)
        self.CardLabel.place(relx=0.094, rely=0.853, height=22, width=40)
        self.CardLabel.configure(activebackground="#f9f9f9")
        self.CardLabel.configure(anchor='w')
        self.CardLabel.configure(background="#d9d9d9")
        self.CardLabel.configure(compound='left')
        self.CardLabel.configure(disabledforeground="#a3a3a3")
        self.CardLabel.configure(foreground="#000000")
        self.CardLabel.configure(highlightbackground="#d9d9d9")
        self.CardLabel.configure(highlightcolor="black")
        self.CardLabel.configure(text='''Card:''')


        ''' Entries Bellow >>>'''
        
        self.NameEntry = tk.Entry(self.CustomerDetailsFrame)
        self.NameEntry.place(relx=0.214, rely=0.109, height=20, relwidth=0.622)
        self.NameEntry.configure(background="white")
        self.NameEntry.configure(disabledforeground="#a3a3a3")
        self.NameEntry.configure(font="TkFixedFont")
        self.NameEntry.configure(foreground="#000000")
        self.NameEntry.configure(highlightbackground="#d9d9d9")
        self.NameEntry.configure(highlightcolor="black")
        self.NameEntry.configure(insertbackground="black")
        self.NameEntry.configure(selectbackground="#c4c4c4")
        self.NameEntry.configure(selectforeground="black")
        
        self.HouseEntry = tk.Entry(self.CustomerDetailsFrame)
        self.HouseEntry.place(relx=0.214, rely=0.217, height=20, relwidth=0.233)
        self.HouseEntry.configure(background="white")
        self.HouseEntry.configure(disabledforeground="#a3a3a3")
        self.HouseEntry.configure(font="TkFixedFont")
        self.HouseEntry.configure(foreground="#000000")
        self.HouseEntry.configure(highlightbackground="#d9d9d9")
        self.HouseEntry.configure(highlightcolor="black")
        self.HouseEntry.configure(insertbackground="black")
        self.HouseEntry.configure(selectbackground="#c4c4c4")
        self.HouseEntry.configure(selectforeground="black")
        
        self.MPEntry = tk.Entry(self.CustomerDetailsFrame)
        self.MPEntry.place(relx=0.214, rely=0.318, height=20, relwidth=0.233)
        self.MPEntry.configure(background="white")
        self.MPEntry.configure(disabledforeground="#a3a3a3")
        self.MPEntry.configure(font="TkFixedFont")
        self.MPEntry.configure(foreground="#000000")
        self.MPEntry.configure(highlightbackground="#d9d9d9")
        self.MPEntry.configure(highlightcolor="black")
        self.MPEntry.configure(insertbackground="black")
        self.MPEntry.configure(selectbackground="#c4c4c4")
        self.MPEntry.configure(selectforeground="black")
        
        self.NumberEntry = tk.Entry(self.CustomerDetailsFrame)
        self.NumberEntry.place(relx=0.214, rely=0.419, height=20, relwidth=0.456)
        self.NumberEntry.configure(background="white")
        self.NumberEntry.configure(disabledforeground="#a3a3a3")
        self.NumberEntry.configure(font="TkFixedFont")
        self.NumberEntry.configure(foreground="#000000")
        self.NumberEntry.configure(highlightbackground="#d9d9d9")
        self.NumberEntry.configure(highlightcolor="black")
        self.NumberEntry.configure(insertbackground="black")
        self.NumberEntry.configure(selectbackground="#c4c4c4")
        self.NumberEntry.configure(selectforeground="black")
        
        self.NLimit = tk.Entry(self.CustomerDetailsFrame)
        self.NLimit.place(relx=0.214, rely=0.527, height=20, relwidth=0.233)
        self.NLimit.configure(background="white")
        self.NLimit.configure(disabledforeground="#a3a3a3")
        self.NLimit.configure(font="TkFixedFont")
        self.NLimit.configure(foreground="#000000")
        self.NLimit.configure(highlightbackground="#d9d9d9")
        self.NLimit.configure(highlightcolor="black")
        self.NLimit.configure(insertbackground="black")
        self.NLimit.configure(selectbackground="#c4c4c4")
        self.NLimit.configure(selectforeground="black")
        
        self.BalanceEntry = tk.Entry(self.CustomerDetailsFrame)
        self.BalanceEntry.place(relx=0.214, rely=0.632, height=20, relwidth=0.233)
        self.BalanceEntry.configure(background="white")
        self.BalanceEntry.configure(disabledforeground="#a3a3a3")
        self.BalanceEntry.configure(font="TkFixedFont")
        self.BalanceEntry.configure(foreground="#000000")
        self.BalanceEntry.configure(highlightbackground="#d9d9d9")
        self.BalanceEntry.configure(highlightcolor="black")
        self.BalanceEntry.configure(insertbackground="black")
        self.BalanceEntry.configure(selectbackground="#c4c4c4")
        self.BalanceEntry.configure(selectforeground="black")
        
        self.DOBEntry = DateEntry(self.CustomerDetailsFrame)
        self.DOBEntry.place(relx=0.214, rely=0.74, height=20, relwidth=0.233)
        self.DOBEntry.configure(state="disabled")
        
        self.CardEntry = tk.Entry(self.CustomerDetailsFrame)
        self.CardEntry.place(relx=0.214, rely=0.849, height=20, relwidth=0.233)
        self.CardEntry.configure(background="white")
        self.CardEntry.configure(disabledforeground="#a3a3a3")
        self.CardEntry.configure(font="TkFixedFont")
        self.CardEntry.configure(foreground="#000000")
        self.CardEntry.configure(highlightbackground="#d9d9d9")
        self.CardEntry.configure(highlightcolor="black")
        self.CardEntry.configure(insertbackground="black")
        self.CardEntry.configure(selectbackground="#c4c4c4")
        self.CardEntry.configure(selectforeground="black")
        self.CardEntry.configure(state="disabled")

        '''<<< entries finished'''
        
        self.CDLabel = tk.Label(self.CustomerFrame)
        self.CDLabel.place(relx=0.306, rely=0.013, height=23, width=135)
        self.CDLabel.configure(activebackground="#f9f9f9")
        self.CDLabel.configure(anchor='w')
        self.CDLabel.configure(background="#d9d9d9")
        self.CDLabel.configure(compound='left')
        self.CDLabel.configure(disabledforeground="#a3a3a3")
        self.CDLabel.configure(foreground="#000000")
        self.CDLabel.configure(highlightbackground="#d9d9d9")
        self.CDLabel.configure(highlightcolor="black")
        self.CDLabel.configure(text='''Customer Details''')
        
        self.EditButton = tk.Button(self.CustomerFrame)
        self.EditButton.place(relx=0.348, rely=0.384, height=44, width=97)
        self.EditButton.configure(activebackground="beige")
        self.EditButton.configure(activeforeground="black")
        self.EditButton.configure(background="#d9d9d9")
        self.EditButton.configure(command=self.Edit_Customer)
        self.EditButton.configure(compound='left')
        self.EditButton.configure(disabledforeground="#a3a3a3")
        self.EditButton.configure(foreground="#000000")
        self.EditButton.configure(highlightbackground="#d9d9d9")
        self.EditButton.configure(highlightcolor="black")
        self.EditButton.configure(pady="0")
        self.EditButton.configure(text='''Edit''')
        
        self.AddButton = tk.Button(self.CustomerFrame)
        self.AddButton.place(relx=0.031, rely=0.384, height=44, width=97)
        self.AddButton.configure(activebackground="beige")
        self.AddButton.configure(activeforeground="black")
        self.AddButton.configure(background="#d9d9d9")
        self.AddButton.configure(command=self.Add_Customer)
        self.AddButton.configure(compound='left')
        self.AddButton.configure(disabledforeground="#a3a3a3")
        self.AddButton.configure(foreground="#000000")
        self.AddButton.configure(highlightbackground="#d9d9d9")
        self.AddButton.configure(highlightcolor="black")
        self.AddButton.configure(pady="0")
        self.AddButton.configure(text='''Add''')
        
        self.DeleteButton = tk.Button(self.CustomerFrame)
        self.DeleteButton.place(relx=0.665, rely=0.384, height=44, width=97)
        self.DeleteButton.configure(activebackground="beige")
        self.DeleteButton.configure(activeforeground="black")
        self.DeleteButton.configure(background="#d9d9d9")
        self.DeleteButton.configure(command=self.Delete_Customer)
        self.DeleteButton.configure(compound='left')
        self.DeleteButton.configure(disabledforeground="#a3a3a3")
        self.DeleteButton.configure(foreground="#000000")
        self.DeleteButton.configure(highlightbackground="#d9d9d9")
        self.DeleteButton.configure(highlightcolor="black")
        self.DeleteButton.configure(pady="0")
        self.DeleteButton.configure(text='''Delete''')
        
        self.TopUPButton = tk.Button(self.CustomerFrame)
        self.TopUPButton.place(relx=0.665, rely=0.452, height=44, width=97)
        self.TopUPButton.configure(activebackground="beige")
        self.TopUPButton.configure(activeforeground="black")
        self.TopUPButton.configure(background="#d9d9d9")
        self.TopUPButton.configure(command=self.TopUP)
        self.TopUPButton.configure(compound='left')
        self.TopUPButton.configure(disabledforeground="#a3a3a3")
        self.TopUPButton.configure(foreground="#000000")
        self.TopUPButton.configure(highlightbackground="#d9d9d9")
        self.TopUPButton.configure(highlightcolor="black")
        self.TopUPButton.configure(pady="0")
        self.TopUPButton.configure(text='''Top-up''')
        
        self.AddCardButton = tk.Button(self.CustomerFrame)
        self.AddCardButton.place(relx=0.031, rely=0.453, height=44, width=97)
        self.AddCardButton.configure(activebackground="beige")
        self.AddCardButton.configure(activeforeground="black")
        self.AddCardButton.configure(background="#d9d9d9")
        self.AddCardButton.configure(command=self.Add_Card)
        self.AddCardButton.configure(compound='left')
        self.AddCardButton.configure(disabledforeground="#a3a3a3")
        self.AddCardButton.configure(foreground="#000000")
        self.AddCardButton.configure(highlightbackground="#d9d9d9")
        self.AddCardButton.configure(highlightcolor="black")
        self.AddCardButton.configure(pady="0")
        self.AddCardButton.configure(text='''Add Card''')
        
        self.RemoveCardButton = tk.Button(self.CustomerFrame)
        self.RemoveCardButton.place(relx=0.348, rely=0.453, height=44, width=97)
        self.RemoveCardButton.configure(activebackground="beige")
        self.RemoveCardButton.configure(activeforeground="black")
        self.RemoveCardButton.configure(background="#d9d9d9")
        self.RemoveCardButton.configure(command=self.Remove_Card)
        self.RemoveCardButton.configure(compound='left')
        self.RemoveCardButton.configure(disabledforeground="#a3a3a3")
        self.RemoveCardButton.configure(foreground="#000000")
        self.RemoveCardButton.configure(highlightbackground="#d9d9d9")
        self.RemoveCardButton.configure(highlightcolor="black")
        self.RemoveCardButton.configure(pady="0")
        self.RemoveCardButton.configure(text='''Remove Card''')
        
        self.CustomerListLabel = tk.Label(self.CustomerFrame)
        self.CustomerListLabel.place(relx=0.369, rely=0.53, height=22, width=99)
        self.CustomerListLabel.configure(anchor='w')
        self.CustomerListLabel.configure(background="#d9d9d9")
        self.CustomerListLabel.configure(compound='left')
        self.CustomerListLabel.configure(disabledforeground="#a3a3a3")
        self.CustomerListLabel.configure(foreground="#000000")
        self.CustomerListLabel.configure(text='''Customer List''')
        
        self.CustomerList = ScrolledFrame(self.CustomerFrame)
        self.CustomerList.place(relx=0.031, rely=0.571, relheight=0.417, relwidth=0.935)
        self.CustomerList.configure(relief='groove')
        self.CustomerList.configure(borderwidth="2")
        self.CustomerList.configure(relief="groove")
        self.CustomerList.configure(background="#d9d9d9")

        '''
        ##CustomerList test
        for i in range(50):
            self.labell = ttk.Label(self.CustomerList.frame, text=f"Label {i}")
            self.labell.pack(padx=10, pady=5)
        self.CustomerList.update_scrollregion()
        '''
        
        self.SalesOuterFrame = tk.Frame(self.top)
        self.SalesOuterFrame.place(relx=0.597, rely=0.013, relheight=0.954, relwidth=0.208)
        self.SalesOuterFrame.configure(relief='groove')
        self.SalesOuterFrame.configure(borderwidth="2")
        self.SalesOuterFrame.configure(relief="groove")
        self.SalesOuterFrame.configure(background="#d9d9d9")
        
        self.SalesList = ScrolledFrame(self.SalesOuterFrame)
        self.SalesList.place(relx=0.043, rely=0.053, relheight=0.932, relwidth=0.92)
        self.SalesList.configure(relief='groove')
        self.SalesList.configure(borderwidth="2")
        self.SalesList.configure(relief="groove")
        self.SalesList.configure(background="#d9d9d9")

        '''
        ##SalesList test
        for i in range(50):
            self.labell = ttk.Label(self.SalesList.frame, text=f"Label {i}")
            self.labell.pack(padx=10, pady=5)
            
        self.SalesList.update_scrollregion()
        '''
        
        self.SalesLabel = tk.Label(self.SalesOuterFrame)
        self.SalesLabel.place(relx=0.428, rely=0.013, height=23, width=40)
        self.SalesLabel.configure(anchor='w')
        self.SalesLabel.configure(background="#d9d9d9")
        self.SalesLabel.configure(compound='left')
        self.SalesLabel.configure(disabledforeground="#a3a3a3")
        self.SalesLabel.configure(foreground="#000000")
        self.SalesLabel.configure(text='''Stock''')
        
        self.PurchasesFrame = tk.Frame(self.top)
        self.PurchasesFrame.place(relx=0.81, rely=0.013, relheight=0.954, relwidth=0.182)
        self.PurchasesFrame.configure(relief='groove')
        self.PurchasesFrame.configure(borderwidth="2")
        self.PurchasesFrame.configure(relief="groove")
        self.PurchasesFrame.configure(background="#d9d9d9")
        
        self.PurchasesLabel = tk.Label(self.PurchasesFrame)
        self.PurchasesLabel.place(relx=0.39, rely=0.013, height=23, width=88)
        self.PurchasesLabel.configure(anchor='w')
        self.PurchasesLabel.configure(background="#d9d9d9")
        self.PurchasesLabel.configure(compound='left')
        self.PurchasesLabel.configure(disabledforeground="#a3a3a3")
        self.PurchasesLabel.configure(foreground="#000000")
        self.PurchasesLabel.configure(text='''Log''')
        
        self.PurchasesList = ScrolledFrame(self.PurchasesFrame)
        self.PurchasesList.place(relx=0.05, rely=0.053, relheight=0.935, relwidth=0.905)
        self.PurchasesList.configure(relief='groove')
        self.PurchasesList.configure(borderwidth="2")
        self.PurchasesList.configure(relief="groove")
        self.PurchasesList.configure(background="#d9d9d9")

        '''
        ##PurchasesList test
        for i in range(50):
            self.labell = ttk.Label(self.PurchasesList.frame, text=f"Label {i}")
            self.labell.pack(padx=10, pady=5)
            
        self.PurchasesList.update_scrollregion()
        '''
        
    def Add_Card(self,*args):
        if _debug:
            print('UI_self.Add_Card')
            for arg in args:
                print ('	another arg:', arg)
            sys.stdout.flush()
            
    def Remove_Card(self,*args):
        if _debug:
            print('UI_self.Remove_Card')
            for arg in args:
                print ('	another arg:', arg)
            sys.stdout.flush()

    def BUY(self,*args):
        if _debug:
            print('UI_self.BUY')
            for arg in args:
                print ('	another arg:', arg)
            sys.stdout.flush()

    def Add_Customer(self,*args):
        if _debug:
            print('UI_self.Add_Customer')
            for arg in args:
                print ('	another arg:', arg)
            sys.stdout.flush()

    def Delete_Customer(self,*args):
        if _debug:
            print('UI_self.Delete_Customer')
            for arg in args:
                print ('	another arg:', arg)
            sys.stdout.flush()

    def Edit_Customer(self,*args):
        if _debug:
            print('UI_self.Edit_Customer')
            for arg in args:
                print ('	another arg:', arg)
            sys.stdout.flush()

    def Pay(self,*args):
        if self.Card:
            if self.Balance >= self.total:
                self.Balance -= self.total
                self.Reset()
                self.BalanceEntry.delete(0,END)
                self.BalanceEntry.insert(0,str(self.Balance))
            else:
                print("not enough balance!")
        else:
            print("no card!")
                
            
    def TopUP(self,*args):
        if _debug:
            print('UI_self.TopUP')
            for arg in args:
                print ('	another arg:', arg)
            sys.stdout.flush()

    def Reset(self,*args):
        self.B1, self.B2, self.B3, self.B5, self.B10, self.B15 = 0,0,0,0,0,0
        self.sub1, self.sub2, self.sub3, self.sub5, self.sub10, self.sub15 = 0,0,0,0,0,0
        self.update_total()
        t = "X   "+str(self.B1)
        self.Z1AmountLabel.configure(text=t)
        t = "X   "+str(self.B2)
        self.Z2AmountLabel.configure(text=t)
        t = "X   "+str(self.B3)
        self.Z3AmountLabel.configure(text=t)
        t = "X   "+str(self.B5)
        self.Z5AmountLabel.configure(text=t)
        t = "X   "+str(self.B10)
        self.Z10AmountLabel.configure(text=t)
        t = "X   "+str(self.B15)
        self.Z15AmountLabel.configure(text=t)
        t = "Sub-total: "+str(self.sub1)
        self.Z1SubtotalLabel.configure(text= t)
        t = "Sub-total: "+str(self.sub2)
        self.Z2SubtotalLabel.configure(text= t)
        t = "Sub-total: "+str(self.sub3)
        self.Z3SubtotalLabel.configure(text= t)
        t = "Sub-total: "+str(self.sub5)
        self.Z5SubtotalLabel.configure(text= t)
        t = "Sub-total: "+str(self.sub10)
        self.Z10SubtotalLabel.configure(text= t)
        t = "Sub-total: "+str(self.sub15)
        self.Z15SubtotalLabel.configure(text= t)

    def update_total(self):
        self.total = self.sub1 + self.sub2 + self.sub3 + self.sub5 + self.sub10 + self.sub15
        t = "Total: " + str(self.total)
        self.TotalLabel.configure(text= t)
   
    def Za2ateet1(self,*args):
        self.B1 += 1
        t = "X   "+str(self.B1)
        self.Z1AmountLabel.configure(text=t)
        self.sub1 = self.B1 * 1
        t = "Sub-total: "+str(self.sub1)
        self.Z1SubtotalLabel.configure(text= t)
        self.update_total()

    def Za2ateet2(self,*args):
        self.B2 += 1
        t = "X   "+str(self.B2)
        self.Z2AmountLabel.configure(text=t)
        self.sub2 = self.B2 * 2
        t = "Sub-total: "+str(self.sub2)
        self.Z2SubtotalLabel.configure(text= t)
        self.update_total()

    def Za2ateet3(self,*args):
        self.B3 += 1
        t = "X   "+str(self.B3)
        self.Z3AmountLabel.configure(text=t)
        self.sub3 = self.B3 * 3
        t = "Sub-total: "+str(self.sub3)
        self.Z3SubtotalLabel.configure(text= t)
        self.update_total()
            
    def Za2ateet5(self,*args):
        self.B5 += 1
        t = "X   "+str(self.B5)
        self.Z5AmountLabel.configure(text=t)
        self.sub5 = self.B5 * 5
        t = "Sub-total: "+str(self.sub5)
        self.Z5SubtotalLabel.configure(text= t)
        self.update_total()

    def Za2ateet10(self,*args):
        self.B10 += 1
        t = "X   "+str(self.B10)
        self.Z10AmountLabel.configure(text=t)
        self.sub10 = self.B10 * 10
        t = "Sub-total: "+str(self.sub10)
        self.Z10SubtotalLabel.configure(text= t)
        self.update_total()

    def Za2ateet15(self,*args):
        self.B15 += 1
        t = "X   "+str(self.B15)
        self.Z15AmountLabel.configure(text=t)
        self.sub15 = self.B15 * 15
        t = "Sub-total: "+str(self.sub15)
        self.Z15SubtotalLabel.configure(text= t)
        self.update_total()

    def Za2ateet1n(self,*args):
        if self.B1 > 0:
            self.B1 -= 1
            t = "X   "+str(self.B1)
            self.Z1AmountLabel.configure(text=t)
            self.sub1 = self.B1 * 1
            t = "Sub-total: "+str(self.sub1)
            self.Z1SubtotalLabel.configure(text= t)
            self.update_total()

    def Za2ateet2n(self,*args):
        if self.B2 > 0:
            self.B2 -= 1
            t = "X   "+str(self.B2)
            self.Z2AmountLabel.configure(text=t)
            self.sub2 = self.B2 * 2
            t = "Sub-total: "+str(self.sub2)
            self.Z2SubtotalLabel.configure(text= t)
            self.update_total()

    def Za2ateet3n(self,*args):
        if self.B3 > 0:
            self.B3 -= 1
            t = "X   "+str(self.B3)
            self.Z3AmountLabel.configure(text=t)
            self.sub3 = self.B3 * 3
            t = "Sub-total: "+str(self.sub3)
            self.Z3SubtotalLabel.configure(text= t)
            self.update_total()

    def Za2ateet5n(self,*args):
        if self.B5 > 0:
            self.B5 -= 1
            t = "X   "+str(self.B5)
            self.Z5AmountLabel.configure(text=t)
            self.sub5 = self.B5 * 5
            t = "Sub-total: "+str(self.sub5)
            self.Z5SubtotalLabel.configure(text= t)
            self.update_total()

    def Za2ateet10n(self,*args):
        if self.B10 > 0:
            self.B10 -= 1
            t = "X   "+str(self.B10)
            self.Z10AmountLabel.configure(text=t)
            self.sub10 = self.B10 * 10
            t = "Sub-total: "+str(self.sub10)
            self.Z10SubtotalLabel.configure(text= t)
            self.update_total()

    def Za2ateet15n(self,*args):
        if self.B15 > 0:
            self.B15 -= 1
            t = "X   "+str(self.B15)
            self.Z15AmountLabel.configure(text=t)
            self.sub15 = self.B15 * 15
            t = "Sub-total: "+str(self.sub15)
            self.Z15SubtotalLabel.configure(text= t)
            self.update_total()

            

if __name__ == '__main__':
    _debug = True
    root = tk.Tk()
    root.protocol( 'WM_DELETE_WINDOW' , root.destroy)
    _top1 = root
    _w1 = Toplevel1(_top1)
    root.mainloop()


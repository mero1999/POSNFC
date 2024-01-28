#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
import tkinter as tk
from datetime import datetime
from tkinter import simpledialog
from tkcalendar import DateEntry
from tkinter.constants import *
from support import *      
    
class Toplevel1:       
    def __init__(self, top=None):
        #user/admin control initialization
        self.user = None
        self.admin = False
        
        #entry_vars
        self.NameEntryText = tk.StringVar()
        self.HouseEntryText = tk.StringVar()   
        self.EmailEntryText = tk.StringVar()
        self.NumberEntryText = tk.StringVar()
        self.NLimitEntryText = tk.StringVar()
        self.BalanceEntryText = tk.StringVar()
        self.DOBEntryText = tk.StringVar()
        self.CardEntryText = tk.StringVar()
              
        #B1,B2,B3,B5,B10,B15 = amount of 1,2,3,5,10,15 za2toot catigories in cart
        self.B1 = 0
        self.B2 = 0
        self.B3 = 0
        self.B5 = 0
        self.B10 = 0
        self.B15 = 0

        #sub1,sub2,sub3,sub5,sub10,sub15 = subtotals in cart
        self.sub1 = 0
        self.sub2 = 0
        self.sub3 = 0
        self.sub5 = 0
        self.sub10 = 0
        self.sub15 = 0
        
        #cart total
        self.total = 0
        
        #init customer data
        self.UID = None
        self.Name = None
        self.House = None
        self.Email = None
        self.Number = None
        self.limit = None
        self.Balance = None
        self.DOB = None
        self.Card = None

        #init db and get all data
        self.db = MyDB(self)
        self.users = self.db.getUsers()
        self.customers = self.db.getCustomers()
        self.stocks = self.db.getStocks()
        self.purchases = self.db.getPurchases()
        
        #init orders list
        self.orders = []
        
        #Menue / Reciept init
        self.reciept = ""
        self.values = {}
        self.stocks = self.db.getStocks()
        
        #start NFC server
        self.nfc = NFC(self)
        
        #configure TopLevel
        top.geometry("1327x832+222+65")
        top.minsize(120, 1)
        top.maxsize(1924, 1061)
        top.resizable(1,  1)
        top.title("Monti-POS Cafeteria System")
        top.configure(background="Black")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")
        self.top = top
                
        #UI starts here
        self.Frame1 = tk.Frame(self.top)
        self.Frame1.place(relx=0.009, rely=0.013, relheight=0.954, relwidth=0.156)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")
        self.Frame1.configure(background="black")
        self.Frame1.configure(highlightbackground="#d9d9d9")
        self.Frame1.configure(highlightcolor="black")
        
        self.Frame2 = tk.Frame(self.Frame1)
        self.Frame2.place(relx=0.058, rely=0.053, relheight=0.841, relwidth=0.884)
        self.Frame2.configure(relief='groove')
        self.Frame2.configure(borderwidth="2")
        self.Frame2.configure(relief="groove")
        self.Frame2.configure(background="black")
        self.Frame2.configure(highlightbackground="#d9d9d9")
        self.Frame2.configure(highlightcolor="black")
        
        self.z1 = HoverButton(self.Frame2)
        self.z1.place(relx=0.115, rely=0.046, height=74, width=137)
        self.z1.configure(command=self.Za2ateet1)
        self.z1.configure(text='''1 Za2toot''')
        
        self.z2 = HoverButton(self.Frame2)
        self.z2.place(relx=0.115, rely=0.205, height=74, width=137)
        self.z2.configure(command=self.Za2ateet2)
        self.z2.configure(text='''2 Za2toot''')
        
        self.z3 = HoverButton(self.Frame2)
        self.z3.place(relx=0.115, rely=0.362, height=74, width=137)
        self.z3.configure(command=self.Za2ateet3)
        self.z3.configure(text='''3 Za2toot''')
        
        self.z5 = HoverButton(self.Frame2)
        self.z5.place(relx=0.115, rely=0.519, height=74, width=137)
        self.z5.configure(command=self.Za2ateet5)
        self.z5.configure(text='''5 Za2toot''')
        
        self.z10 = HoverButton(self.Frame2)
        self.z10.place(relx=0.115, rely=0.677, height=74, width=137)
        self.z10.configure(command=self.Za2ateet10)
        self.z10.configure(text='''10 Za2toot''')
        
        self.z15 = HoverButton(self.Frame2)
        self.z15.place(relx=0.115, rely=0.835, height=74, width=137)
        self.z15.configure(command=self.Za2ateet15)
        self.z15.configure(text='''15 Za2toot''')
        
        self.BuyButton = HoverButton(self.Frame1, overrelief='groove')
        self.BuyButton.place(relx=0.065, rely=0.901, height=64, width=175)
        self.BuyButton.configure(command=self.BUY)
        self.BuyButton.configure(text='''Buy''')
        
        self.ItemsLabel = Label(self.Frame1)
        self.ItemsLabel.place(relx=0.335, rely=0.013, height=30, width=80)
        self.ItemsLabel.configure(text='''Specials''')
        
        self.CartFrame = tk.Frame(self.top)
        self.CartFrame.place(relx=0.169, rely=0.013, relheight=0.954, relwidth=0.126)
        self.CartFrame.configure(relief='groove')
        self.CartFrame.configure(borderwidth="2")
        self.CartFrame.configure(relief="groove")
        self.CartFrame.configure(background="black")
        self.CartFrame.configure(highlightbackground="#d9d9d9")
        self.CartFrame.configure(highlightcolor="black")
        
        self.SubtotalFrame = tk.Frame(self.CartFrame)
        self.SubtotalFrame.place(relx=0.06, rely=0.053, relheight=0.841, relwidth=0.886)
        self.SubtotalFrame.configure(relief='groove')
        self.SubtotalFrame.configure(borderwidth="2")
        self.SubtotalFrame.configure(relief="groove")
        self.SubtotalFrame.configure(background="black")
        self.SubtotalFrame.configure(highlightbackground="#d9d9d9")
        self.SubtotalFrame.configure(highlightcolor="black")
        
        self.Z1AmountLabel = Label(self.SubtotalFrame)
        self.Z1AmountLabel.place(relx=0.081, rely=0.079, height=23, width=40)
        self.Z1AmountLabel.configure(text='''X   0''')  
        self.Z1AmountLabel.configure(font=("forte", 10))  
        
        self.Z2AmountLabel = Label(self.SubtotalFrame)
        self.Z2AmountLabel.place(relx=0.081, rely=0.237, height=23, width=40)
        self.Z2AmountLabel.configure(text='''X   0''')
        self.Z2AmountLabel.configure(font=("forte", 10)) 
        
        self.Z3AmountLabel = Label(self.SubtotalFrame)
        self.Z3AmountLabel.place(relx=0.081, rely=0.394, height=23, width=40)
        self.Z3AmountLabel.configure(text='''X   0''')
        self.Z3AmountLabel.configure(font=("forte", 10)) 
        
        self.Z5AmountLabel = Label(self.SubtotalFrame)
        self.Z5AmountLabel.place(relx=0.081, rely=0.551, height=23, width=40)
        self.Z5AmountLabel.configure(text='''X   0''')
        self.Z5AmountLabel.configure(font=("forte", 10)) 
        
        self.Z10AmountLabel = Label(self.SubtotalFrame)
        self.Z10AmountLabel.place(relx=0.081, rely=0.71, height=23, width=40)
        self.Z10AmountLabel.configure(text='''X   0''')
        self.Z10AmountLabel.configure(font=("forte", 10)) 
        
        self.Z15AmountLabel = Label(self.SubtotalFrame)
        self.Z15AmountLabel.place(relx=0.081, rely=0.865, height=23, width=40)
        self.Z15AmountLabel.configure(text='''X   0''')
        self.Z15AmountLabel.configure(font=("forte", 10)) 

        self.Z1SubtotalLabel = Label(self.SubtotalFrame)
        self.Z1SubtotalLabel.configure(text='''Sub-total: 0''')
        self.Z1SubtotalLabel.place(relx=0.081, rely=0.115, height=22, width=87)
        self.Z1SubtotalLabel.configure(font=("forte", 10)) 
        
        self.Z2SubtotalLabel = Label(self.SubtotalFrame)
        self.Z2SubtotalLabel.place(relx=0.081, rely=0.268, height=22, width=87)
        self.Z2SubtotalLabel.configure(text='''Sub-total: 0''')
        self.Z2SubtotalLabel.configure(font=("forte", 10)) 
        
        self.Z3SubtotalLabel = Label(self.SubtotalFrame)
        self.Z3SubtotalLabel.place(relx=0.081, rely=0.425, height=22, width=87)
        self.Z3SubtotalLabel.configure(text='''Sub-total: 0''')
        self.Z3SubtotalLabel.configure(font=("forte", 10)) 
        
        self.Z5SubtotalLabel = Label(self.SubtotalFrame)
        self.Z5SubtotalLabel.configure(text='''Sub-total: 0''')
        self.Z5SubtotalLabel.place(relx=0.081, rely=0.574, height=22, width=87)
        self.Z5SubtotalLabel.configure(font=("forte", 10)) 
        
        self.Z10SubtotalLabel = Label(self.SubtotalFrame)
        self.Z10SubtotalLabel.place(relx=0.081, rely=0.74, height=22, width=87)
        self.Z10SubtotalLabel.configure(text='''Sub-total: 0''')
        self.Z10SubtotalLabel.configure(font=("forte", 10)) 
        
        self.Z15SubtotalLabel = Label(self.SubtotalFrame)
        self.Z15SubtotalLabel.place(relx=0.081, rely=0.898, height=22, width=87)
        self.Z15SubtotalLabel.configure(text='''Sub-total: 0''')
        self.Z15SubtotalLabel.configure(font=("forte", 10))
        
        self.Z1nButton = tk.Button(self.SubtotalFrame)
        self.Z1nButton.place(relx=0.797, rely=0.079, height=24, width=17)
        self.Z1nButton.configure(activebackground="black")
        self.Z1nButton.configure(activeforeground="black")
        self.Z1nButton.configure(background="black")
        self.Z1nButton.configure(command=self.Za2ateet1n)
        self.Z1nButton.configure(compound='left')
        self.Z1nButton.configure(disabledforeground="#89CFF0")
        self.Z1nButton.configure(foreground="#89CFF0")
        self.Z1nButton.configure(bd=0)
        self.Z1nButton.configure(font=("Arial",40))
        self.Z1nButton.configure(highlightbackground="#89CFF0")
        self.Z1nButton.configure(highlightcolor="black")
        self.Z1nButton.configure(pady="0")
        self.Z1nButton.configure(text='''-''')
        
        self.Z2nButton = tk.Button(self.SubtotalFrame)
        self.Z2nButton.place(relx=0.797, rely=0.237, height=24, width=17)
        self.Z2nButton.configure(activebackground="black")
        self.Z2nButton.configure(activeforeground="black")
        self.Z2nButton.configure(background="black")
        self.Z2nButton.configure(command=self.Za2ateet2n)
        self.Z2nButton.configure(compound='left')
        self.Z2nButton.configure(bd=0)
        self.Z2nButton.configure(font=("Arial",40))
        self.Z2nButton.configure(disabledforeground="#89CFF0")
        self.Z2nButton.configure(foreground="#89CFF0")
        self.Z2nButton.configure(highlightbackground="#89CFF0")
        self.Z2nButton.configure(highlightcolor="black")
        self.Z2nButton.configure(pady="0")
        self.Z2nButton.configure(text='''-''')
        
        self.Z3nButton = tk.Button(self.SubtotalFrame)
        self.Z3nButton.place(relx=0.797, rely=0.394, height=24, width=17)
        self.Z3nButton.configure(activebackground="black")
        self.Z3nButton.configure(activeforeground="black")
        self.Z3nButton.configure(background="black")
        self.Z3nButton.configure(command=self.Za2ateet3n)
        self.Z3nButton.configure(compound='left')
        self.Z3nButton.configure(bd=0)
        self.Z3nButton.configure(font=("Arial",40))
        self.Z3nButton.configure(disabledforeground="#89CFF0")
        self.Z3nButton.configure(foreground="#89CFF0")
        self.Z3nButton.configure(highlightbackground="#89CFF0")
        self.Z3nButton.configure(highlightcolor="black")
        self.Z3nButton.configure(pady="0")
        self.Z3nButton.configure(text='''-''')
        
        self.Z5nButton = tk.Button(self.SubtotalFrame)
        self.Z5nButton.place(relx=0.797, rely=0.551, height=24, width=17)
        self.Z5nButton.configure(activebackground="black")
        self.Z5nButton.configure(activeforeground="black")
        self.Z5nButton.configure(background="black")
        self.Z5nButton.configure(command=self.Za2ateet5n)
        self.Z5nButton.configure(compound='left')
        self.Z5nButton.configure(bd=0)
        self.Z5nButton.configure(font=("Arial",40))
        self.Z5nButton.configure(disabledforeground="#89CFF0")
        self.Z5nButton.configure(foreground="#89CFF0")
        self.Z5nButton.configure(highlightbackground="#89CFF0")
        self.Z5nButton.configure(highlightcolor="black")
        self.Z5nButton.configure(pady="0")
        self.Z5nButton.configure(text='''-''')
        
        self.Z10nButton = tk.Button(self.SubtotalFrame)
        self.Z10nButton.place(relx=0.797, rely=0.71, height=24, width=17)
        self.Z10nButton.configure(activebackground="black")
        self.Z10nButton.configure(activeforeground="black")
        self.Z10nButton.configure(background="black")
        self.Z10nButton.configure(command=self.Za2ateet10n)
        self.Z10nButton.configure(compound='left')
        self.Z10nButton.configure(bd=0)
        self.Z10nButton.configure(font=("Arial",40))
        self.Z10nButton.configure(disabledforeground="#89CFF0")
        self.Z10nButton.configure(foreground="#89CFF0")
        self.Z10nButton.configure(highlightbackground="#89CFF0")
        self.Z10nButton.configure(highlightcolor="black")
        self.Z10nButton.configure(pady="0")
        self.Z10nButton.configure(text='''-''')
        
        self.Z15nButton = tk.Button(self.SubtotalFrame)
        self.Z15nButton.place(relx=0.797, rely=0.865, height=24, width=17)
        self.Z15nButton.configure(activebackground="black")
        self.Z15nButton.configure(activeforeground="black")
        self.Z15nButton.configure(background="black")
        self.Z15nButton.configure(command=self.Za2ateet15n)
        self.Z15nButton.configure(compound='left')
        self.Z15nButton.configure(bd=0)
        self.Z15nButton.configure(font=("Arial",40))
        self.Z15nButton.configure(disabledforeground="#89CFF0")
        self.Z15nButton.configure(foreground="#89CFF0")
        self.Z15nButton.configure(highlightbackground="#89CFF0")
        self.Z15nButton.configure(highlightcolor="black")
        self.Z15nButton.configure(pady="0")
        self.Z15nButton.configure(text='''-''')

        self.ResetButton = HoverButton(self.CartFrame,overrelief='groove')
        self.ResetButton.place(relx=0.054, rely=0.905, height=65, width=145)
        self.ResetButton.configure(command=self.Reset)
        self.ResetButton.configure(text='''Reset''')
        
        self.CartLabel = Label(self.CartFrame)
        self.CartLabel.place(relx=0.383, rely=0.013, height=23, width=40)
        self.CartLabel.configure(text='''Cart''')
        
        self.CustomerFrame = tk.Frame(self.top)
        self.CustomerFrame.place(relx=0.303, rely=0.013, relheight=0.954, relwidth=0.29)
        self.CustomerFrame.configure(relief='groove')
        self.CustomerFrame.configure(borderwidth="2")
        self.CustomerFrame.configure(relief="groove")
        self.CustomerFrame.configure(background="black")
        self.CustomerFrame.configure(highlightbackground="#d9d9d9")
        self.CustomerFrame.configure(highlightcolor="black")
        
        self.CustomerDetailsFrame = tk.Frame(self.CustomerFrame)
        self.CustomerDetailsFrame.place(relx=0.031, rely=0.053, relheight=0.325, relwidth=0.935)
        self.CustomerDetailsFrame.configure(relief='groove')
        self.CustomerDetailsFrame.configure(borderwidth="2")
        self.CustomerDetailsFrame.configure(relief="groove")
        self.CustomerDetailsFrame.configure(background="black")
        self.CustomerDetailsFrame.configure(highlightbackground="#d9d9d9")
        self.CustomerDetailsFrame.configure(highlightcolor="black")
        
        self.NameLabel = Label(self.CustomerDetailsFrame)
        self.NameLabel.place(relx=0.072, rely=0.062, height=45, width=52)
        self.NameLabel.configure(text='''Name:''')
        self.NameLabel.configure(font=("forte", 10)) 
        
        self.HouseLabel = Label(self.CustomerDetailsFrame)
        self.HouseLabel.place(relx=0.067, rely=0.194, height=33, width=52)
        self.HouseLabel.configure(font=("forte", 10)) 
        self.HouseLabel.configure(text='''House:''')
        
        self.EmailLabel = Label(self.CustomerDetailsFrame)
        self.EmailLabel.place(relx=0.07, rely=0.295, height=34, width=75)
        self.EmailLabel.configure(font=("forte", 10)) 
        self.EmailLabel.configure(text='''Email:''')
        
        self.NumberLabel = Label(self.CustomerDetailsFrame)
        self.NumberLabel.place(relx=0.033, rely=0.395, height=34, width=64)
        self.NumberLabel.configure(font=("forte", 10)) 
        self.NumberLabel.configure(text='''Number:''')
        
        self.LimitLabel = Label(self.CustomerDetailsFrame)
        self.LimitLabel.place(relx=0.042, rely=0.496, height=35, width=64)
        self.LimitLabel.configure(font=("forte", 10)) 
        self.LimitLabel.configure(text='''N-Limit:''')
        
        self.BalanceLabel = Label(self.CustomerDetailsFrame)
        self.BalanceLabel.place(relx=0.042, rely=0.636, height=22, width=64)
        self.BalanceLabel.configure(font=("forte", 10)) 
        self.BalanceLabel.configure(text='''Balance:''')

        self.DOBLabel = Label(self.CustomerDetailsFrame)
        self.DOBLabel.place(relx=0.078, rely=0.744, height=22, width=52)
        self.DOBLabel.configure(font=("forte", 10)) 
        self.DOBLabel.configure(text='''D.O.B:''')

        self.CardLabel = Label(self.CustomerDetailsFrame)
        self.CardLabel.place(relx=0.094, rely=0.853, height=22, width=40)
        self.CardLabel.configure(font=("forte", 10)) 
        self.CardLabel.configure(text='''Card:''')


        # Entries Start >>>
        self.NameEntry = tk.Entry(self.CustomerDetailsFrame, textvariable=self.NameEntryText)
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
        self.NameEntry.configure(state="readonly")
        
        self.HouseEntry = tk.Entry(self.CustomerDetailsFrame, textvariable=self.HouseEntryText)
        self.HouseEntry.place(relx=0.214, rely=0.217, height=20, relwidth=0.622)
        self.HouseEntry.configure(background="white")
        self.HouseEntry.configure(disabledforeground="#a3a3a3")
        self.HouseEntry.configure(font="TkFixedFont")
        self.HouseEntry.configure(foreground="#000000")
        self.HouseEntry.configure(highlightbackground="#d9d9d9")
        self.HouseEntry.configure(highlightcolor="black")
        self.HouseEntry.configure(insertbackground="black")
        self.HouseEntry.configure(selectbackground="#c4c4c4")
        self.HouseEntry.configure(selectforeground="black")
        self.HouseEntry.configure(state="readonly")
        
        self.EmailEntry = tk.Entry(self.CustomerDetailsFrame, textvariable=self.EmailEntryText)
        self.EmailEntry.place(relx=0.214, rely=0.318, height=20, relwidth=0.622)
        self.EmailEntry.configure(background="white")
        self.EmailEntry.configure(disabledforeground="#a3a3a3")
        self.EmailEntry.configure(font="TkFixedFont")
        self.EmailEntry.configure(foreground="#000000")
        self.EmailEntry.configure(highlightbackground="#d9d9d9")
        self.EmailEntry.configure(highlightcolor="black")
        self.EmailEntry.configure(insertbackground="black")
        self.EmailEntry.configure(selectbackground="#c4c4c4")
        self.EmailEntry.configure(selectforeground="black")
        self.EmailEntry.configure(state="readonly")
        
        self.NumberEntry = tk.Entry(self.CustomerDetailsFrame, textvariable=self.NumberEntryText)
        self.NumberEntry.place(relx=0.214, rely=0.419, height=20, relwidth=0.622)
        self.NumberEntry.configure(background="white")
        self.NumberEntry.configure(disabledforeground="#a3a3a3")
        self.NumberEntry.configure(font="TkFixedFont")
        self.NumberEntry.configure(foreground="#000000")
        self.NumberEntry.configure(highlightbackground="#d9d9d9")
        self.NumberEntry.configure(highlightcolor="black")
        self.NumberEntry.configure(insertbackground="black")
        self.NumberEntry.configure(selectbackground="#c4c4c4")
        self.NumberEntry.configure(selectforeground="black")
        self.NumberEntry.configure(state="readonly")
        
        self.NLimit = tk.Entry(self.CustomerDetailsFrame, textvariable=self.NLimitEntryText)
        self.NLimit.place(relx=0.214, rely=0.527, height=20, relwidth=0.622)
        self.NLimit.configure(background="white")
        self.NLimit.configure(disabledforeground="#a3a3a3")
        self.NLimit.configure(font="TkFixedFont")
        self.NLimit.configure(foreground="#000000")
        self.NLimit.configure(highlightbackground="#d9d9d9")
        self.NLimit.configure(highlightcolor="black")
        self.NLimit.configure(insertbackground="black")
        self.NLimit.configure(selectbackground="#c4c4c4")
        self.NLimit.configure(selectforeground="black")
        self.NLimit.configure(state="readonly")
        
        self.BalanceEntry = tk.Entry(self.CustomerDetailsFrame, textvariable=self.BalanceEntryText)
        self.BalanceEntry.place(relx=0.214, rely=0.632, height=20, relwidth=0.622)
        self.BalanceEntry.configure(background="white")
        self.BalanceEntry.configure(disabledforeground="#a3a3a3")
        self.BalanceEntry.configure(font="TkFixedFont")
        self.BalanceEntry.configure(foreground="#000000")
        self.BalanceEntry.configure(highlightbackground="#d9d9d9")
        self.BalanceEntry.configure(highlightcolor="black")
        self.BalanceEntry.configure(insertbackground="black")
        self.BalanceEntry.configure(selectbackground="#c4c4c4")
        self.BalanceEntry.configure(selectforeground="black")
        self.BalanceEntry.configure(state="readonly")
        
        self.DOBEntry = DateEntry(self.CustomerDetailsFrame, textvariable=self.DOBEntryText, date_pattern="dd-mm-yyyy")
        self.DOBEntry.place(relx=0.214, rely=0.74, height=20, relwidth=0.622)
        self.DOBEntry.configure(state="disabled")
        self.DOBEntry.configure(background="black")
        self.DOBEntry.configure(foreground="gold")
        self.BalanceEntry.configure(selectbackground="pink")
        self.BalanceEntry.configure(selectforeground="blue")
        self.BalanceEntry.configure(highlightbackground="yellow")
        self.BalanceEntry.configure(highlightcolor="green")
        self.BalanceEntry.configure(insertbackground="black")
        self.BalanceEntry.configure(font="Arial")
        
        self.CardEntry = tk.Entry(self.CustomerDetailsFrame, textvariable=self.CardEntryText)
        self.CardEntry.place(relx=0.214, rely=0.849, height=20, relwidth=0.622)
        self.CardEntry.configure(background="white")
        self.CardEntry.configure(disabledforeground="#a3a3a3")
        self.CardEntry.configure(font="TkFixedFont")
        self.CardEntry.configure(foreground="#000000")
        self.CardEntry.configure(highlightbackground="#d9d9d9")
        self.CardEntry.configure(highlightcolor="black")
        self.CardEntry.configure(insertbackground="black")
        self.CardEntry.configure(selectbackground="#c4c4c4")
        self.CardEntry.configure(selectforeground="black")
        self.CardEntry.configure(state="readonly")
        #entries finished
        
        self.CDLabel = Label(self.CustomerFrame)
        self.CDLabel.place(relx=0.30, rely=0.013, height=23, width=155)
        self.CDLabel.configure(text='''Customer Details''')
        
        self.EditButton = HoverButton(self.CustomerFrame)
        self.EditButton.place(relx=0.378, rely=0.384, height=44, width=100)
        self.EditButton.configure(command=self.Edit_Customer)
        self.EditButton.configure(font=("forte", 11))
        self.EditButton.configure(text='''Edit Customer''')
        
        self.AddButton = HoverButton(self.CustomerFrame)
        self.AddButton.place(relx=0.051, rely=0.384, height=44, width=100)
        self.AddButton.configure(command=self.Add_Customer)
        self.AddButton.configure(font=("forte", 11))
        self.AddButton.configure(text='''Add Customer''')
        
        self.DeleteButton = HoverButton(self.CustomerFrame)
        self.DeleteButton.place(relx=0.695, rely=0.384, height=44, width=100)
        self.DeleteButton.configure(command=self.Delete_Customer)
        self.DeleteButton.configure(font=("forte", 10))
        self.DeleteButton.configure(text='''Delete Customer''')
        
        self.TopUPButton = HoverButton(self.CustomerFrame)
        self.TopUPButton.place(relx=0.695, rely=0.453, height=44, width=100)
        self.TopUPButton.configure(command=self.TopUP)
        self.TopUPButton.configure(font=("forte", 12))
        self.TopUPButton.configure(text='''Top-up''')
        
        self.AddCardButton = HoverButton(self.CustomerFrame)
        self.AddCardButton.place(relx=0.051, rely=0.453, height=44, width=100)
        self.AddCardButton.configure(command=self.Add_Card)
        self.AddCardButton.configure(font=("forte", 12))
        self.AddCardButton.configure(text='''Add Card''')
        
        self.RemoveCardButton = HoverButton(self.CustomerFrame)
        self.RemoveCardButton.place(relx=0.378, rely=0.453, height=44, width=100)
        self.RemoveCardButton.configure(command=self.Remove_Card)
        self.RemoveCardButton.configure(font=("forte", 12))
        self.RemoveCardButton.configure(text='''Remove Card''')
        
        self.CustomerListLabel = Label(self.CustomerFrame)
        self.CustomerListLabel.place(relx=0.350, rely=0.53, height=22, width=120)
        self.CustomerListLabel.configure(text='''Customer List''')
        
        self.CustomerList = ScrolledTable(self.CustomerFrame, self)
        self.CustomerList.place(relx=0.031, rely=0.571, relheight=0.417, relwidth=0.935)
        self.CustomerList.configure(relief='groove')
        self.CustomerList.configure(borderwidth="2")
        self.CustomerList.configure(relief="groove")
        
        self.StockOuterFrame = tk.Frame(self.top)
        self.StockOuterFrame.place(relx=0.597, rely=0.013, relheight=0.954, relwidth=0.208)
        self.StockOuterFrame.configure(relief='groove')
        self.StockOuterFrame.configure(borderwidth="2")
        self.StockOuterFrame.configure(relief="groove")
        self.StockOuterFrame.configure(background="black")
        
        self.StocksList = ScrolledFrame(self.StockOuterFrame)
        self.StocksList.place(relx=0.043, rely=0.053, relheight=0.932, relwidth=0.92)
        self.StocksList.configure(relief='groove')
        self.StocksList.configure(borderwidth="2")
        self.StocksList.configure(relief="groove")
        self.StocksList.configure(background="black")
   
        self.StocksLabel = Label(self.StockOuterFrame)
        self.StocksLabel.place(relx=0.388, rely=0.013, height=23, width=62)
        self.StocksLabel.configure(text='''Menu''')

        for stock in self.stocks:
            self.values[stock] = tk.IntVar(value=0)  # Initialize values to 0
            split = tk.Label(self.StocksList.frame, text="  ")
            split.pack(padx=10, pady=3)
            stock1 = ttk.Frame(self.StocksList.frame)
            stock1.pack(padx=3, pady=8)
            name_label = tk.Label(stock1, text=stock[0])
            name_label.pack(padx=10, pady=3)            
            add_button = tk.Button(stock1, text="+", width=3, command=lambda s=stock: self.increment(s))
            add_button.pack(side="left")
            amount_label = tk.Label(stock1, textvariable=self.values[stock], width=23)
            amount_label.pack(side="left")
            reduce_button = tk.Button(stock1, text="-", width=3, command=lambda s=stock: self.decrement(s))
            reduce_button.pack(side="left")            
            split = tk.Label(self.StocksList.frame, text="----------------------------------")
            split.pack(padx=10, pady=3)       
        self.StocksList.update_scrollregion()
        
        self.LogFrame = tk.Frame(self.top)
        self.LogFrame.place(relx=0.81, rely=0.013, relheight=0.954, relwidth=0.182)
        self.LogFrame.configure(relief='groove')
        self.LogFrame.configure(borderwidth="2")
        self.LogFrame.configure(relief="groove")
        self.LogFrame.configure(background="black")
        
        self.LogLabel = tk.Label(self.LogFrame)
        self.LogLabel.place(relx=0.42, rely=0.013, height=23, width=88)
        self.LogLabel.configure(anchor='w')
        self.LogLabel.configure(background="black")
        self.LogLabel.configure(compound='left')
        self.LogLabel.configure(disabledforeground="black")
        self.LogLabel.configure(foreground="Gold")
        self.LogLabel.configure(font=("forte", 14))
        self.LogLabel.configure(text='''Log''')
        
        self.LogList = Log(self.LogFrame, max_length=100)
        self.LogList.place(relx=0.05, rely=0.053, relheight=0.400, relwidth=0.905)
        self.LogList.configure(relief='groove')
        self.LogList.configure(borderwidth="2")
        self.LogList.configure(relief="groove")
        self.LogList.configure(background="black")
        
        self.ordersLabel = tk.Label(self.LogFrame)
        self.ordersLabel.place(relx=0.39, rely=0.465, height=23, width=88)
        self.ordersLabel.configure(anchor='w')
        self.ordersLabel.configure(font=("forte", 14))
        self.ordersLabel.configure(background="black")
        self.ordersLabel.configure(compound='left')
        self.ordersLabel.configure(disabledforeground="black")
        self.ordersLabel.configure(foreground="Gold")
        self.ordersLabel.configure(text='''Orders''')
        
        self.orderListHolder = ScrolledFrame(self.LogFrame)
        self.orderListHolder.place(relx=0.05, rely=0.500, relheight=0.4, relwidth=0.905) 
        
        self.orderList = ScrolledFrame(self.LogFrame)
        self.orderList.place(relx=0.05, rely=0.500, relheight=0.4, relwidth=0.905) 
        self.orderList.update_scrollregion()
        
        self.AddOrderButton = HoverButton(self.LogFrame)
        self.AddOrderButton.place(relx=0.15, rely=0.909, relheight=0.072, relwidth=0.700)
        self.AddOrderButton.configure(command=self.addOrder)
        self.AddOrderButton.configure(text='''Add Order''')
        
        self.Reset()
        
    def addOrder(self):
        if self.UID and self.user:
            if (self.Balance + self.limit) >= self.tot: 
                self.orders.append(self.reciept)
                # Update the displayed orders
                self.updateOrderList()
                self.Reset()
        elif self.UID and not self.user:
            self.Logger("Login required!")
        elif not self.UID and not self.user:
            self.Logger("Unothorized Access Trial!")
            pass
        else:
            self.Logger("Customer selection required!",verbose=True)
            
    def updateOrderList(self):
        # Clear the existing orders in the GUI
        for widget in self.orderList.frame.winfo_children():
            widget.destroy()

        # Add the updated orders to the GUI
        for order in self.orders:
            # Skip first 3 lines and last 2 lines
            order_lines = order.split('\n')[0:-2]

            orderframe = ttk.Frame(self.orderList.frame)
            orderframe.pack(padx=3, pady=3)

            for line in order_lines:
                orderText = tk.Label(orderframe, text=line)
                orderText.pack(padx=10, pady=3)

            confirm_button = tk.Button(orderframe, text="confirm", width=20, command=lambda o=order: self.payOrder(o), bg="green", fg="white", activeforeground="black")
            confirm_button.pack(padx=10, pady=3)
            confirm_button.bind("<Enter>", lambda event, button=confirm_button: button.config(fg="black"))
            confirm_button.bind("<Leave>", lambda event, button=confirm_button: button.config(fg="white"))

            cancel_button = tk.Button(orderframe, text="cancel", width=20, command=lambda o=order: self.cancelOrder(o), bg="red", fg="white", activeforeground="black")
            cancel_button.pack(padx=10, pady=1)
            cancel_button.bind("<Enter>", lambda event, button=cancel_button: button.config(fg="black"))
            cancel_button.bind("<Leave>", lambda event, button=cancel_button: button.config(fg="white"))

            split = tk.Label(self.orderList.frame, text="----------------------------------")
            split.pack(padx=10, pady=2)
            
        # Update the scroll region after adding new widgets
        self.orderList.update_scrollregion()
    
    def payOrder(self, order):
        customer = self.db.getCustomerID(str(order[0]))[0]
        balance = customer[7]
        limit = customer[6]
        amount = int(order.split('\n')[-3].split(': ')[1])

        if self.user:
            # Check if the customer has enough balance
            if (balance + limit) >= amount:
                try:
                    # Update the customer balance in the database
                    self.db.editCustomer(customer[0], None, None, None, None, None, None, balance - amount, None)
                    # Add sale record to the database
                    self.db.addSale(str(self.user), customer[0], amount, order)
                    #Log the transaction
                    self.Logger(f"Payment:\n Amount: {amount}\n Customer: {customer[3]}\n Successful!", verbose=True)
                    # Remove the order from the list
                    self.orders.remove(order)
                    # Update the order list in the GUI
                    self.updateOrderList()
                    # Reset GUI
                    self.Reset()
                except Exception as e:
                    self.Logger(f"Payment:\n Amount: {amount}\n Customer: {customer[3]}\n Unsuccessful!\nError: {str(e)}", verbose=True)
            else:
                self.Logger("Not enough balance!", verbose=True)
        elif self.UID and not self.user:
            self.Logger("Login required!")
        elif not self.UID and not self.user:
            self.Logger("Unauthorized Access Trial!")
        else:
            self.Logger("Customer selection required!", verbose=True)

    def cancelOrder(self, order):
        if self.user:
            # Remove the order from the list
            self.orders.remove(order)
            # Update the order list in the GUI
            self.updateOrderList()
        
    def update_reciept(self):
        if self.user and self.Name:
            self.reciept = str(self.UID) + "\nCustomer: " + self.Name
            self.tot = 0
            for stock_name, stock_value in self.values.items():
                if int(stock_value.get()) > 0:   
                    self.reciept += "\n" + str(stock_name[0]) + " x " + str(stock_name[1]) + "$ x " + str(stock_value.get()) 
                    self.tot += int(stock_name[1]) * int(stock_value.get())
            if self.B1 > 0:
                self.reciept += "\n" + "Special 1 x 1$ x " + str(self.B1)
            if self.B2 > 0:
                self.reciept += "\n" + "Special 2 x 2$ x " + str(self.B2)
            if self.B3 > 0:
                self.reciept += "\n" + "Special 3 x 3$ x " + str(self.B3)
            if self.B5 > 0:
                self.reciept += "\n" + "Special 5 x 5$ x " + str(self.B5)
            if self.B10 > 0:
                self.reciept += "\n" + "Special 10 x 10$ x " + str(self.B10)
            if self.B15 > 0:
                self.reciept += "\n" + "Special 15 x 15$ x " + str(self.B15)
            self.tot += self.total
            self.reciept += "\nTotal: " + str(self.tot)
            self.reciept += "\nBalance Before: " + str(self.Balance)
            self.reciept += "\nBalance After: " + str(self.Balance - self.tot)
            
    def increment(self, stock):
        if self.user and self.Name:
            current_value = int(self.values[stock].get())
            self.values[stock].set(str(current_value + 1))
            self.update_reciept()                      
               
    def decrement(self, stock):
        if self.user and self.Name:
            current_value = int(self.values[stock].get())
            if current_value > 0:
                self.values[stock].set(str(current_value - 1))
                self.update_reciept()    
        
    def Add_Card(self):
        if self.Card and self.user:
            try:
                self.db.editCustomer(self.UID, self.House, self.Card, self.Name, self.DOB, self.Number, self.limit, self.Balance, self.Email)
                self.Logger(f"Card: {self.Card} \nAdded to UID: {self.UID}") 
                self.Logger(f"Done!", verbose = True) 
            except:
                self.Logger(f"Unable to add Card!", verbose = True) 

    def Remove_Card(self):
        if self.Card and self.user:
            self.Card = ""
            try:  
                self.db.editCustomer(self.UID, self.House, self.Card, self.Name, self.DOB, self.Number, self.limit, self.Balance, self.Email)
                self.Logger("Card deleted successfully!",verbose=True)
            except:
                self.Logger("Card does not exist!",verbose=True) 

    def add_Last_Stock(self):
        self.stocks = self.db.getStocks()
        stock = self.stocks[len(self.stocks)-1]
        self.values[stock] = tk.IntVar(value=0)  # Initialize values to 0
        split = tk.Label(self.StocksList.frame, text="----------------------------------")
        split.pack(padx=10, pady=3)
        stock1 = ttk.Frame(self.StocksList.frame)
        stock1.pack(padx=3, pady=8)
        name_label = tk.Label(stock1, text=stock[0])
        name_label.pack(padx=10, pady=3)            
        add_button = tk.Button(stock1, text="+", width=3, command=lambda s=stock: self.increment(s))
        add_button.pack(side="left")
        amount_label = tk.Label(stock1, textvariable=self.values[stock], width=23)
        amount_label.pack(side="left")
        reduce_button = tk.Button(stock1, text="-", width=3, command=lambda s=stock: self.decrement(s))
        reduce_button.pack(side="left")            
        split = tk.Label(self.StocksList.frame, text="----------------------------------")
        split.pack(padx=10, pady=3)       
        self.StocksList.update_scrollregion()
        
    def BUY(self):
        if self.user:
            self.Reset()
            a = StockEntryForm(self.user, self)
            a.start()     
        
    def refreshMenu(self):
        self.stocks = self.db.getStocks()
        # Clear the existing stocks in the GUI
        for widget in self.StocksList.frame.winfo_children():
            widget.destroy()
        for stock in self.stocks:
            self.values[stock] = tk.IntVar(value=1)  
            split = tk.Label(self.StocksList.frame, text="  ")
            split.pack(padx=10, pady=3)
            stock1 = ttk.Frame(self.StocksList.frame)
            stock1.pack(padx=3, pady=8)
            name_label = tk.Label(stock1, text=stock[0])
            name_label.pack(padx=10, pady=3)            
            add_button = tk.Button(stock1, text="+", width=3, command=lambda s=stock: self.increment(s))
            add_button.pack(side="left")
            amount_label = tk.Label(stock1, textvariable=self.values[stock], width=23)
            amount_label.pack(side="left")
            reduce_button = tk.Button(stock1, text="-", width=3, command=lambda s=stock: self.decrement(s))
            reduce_button.pack(side="left")            
            split = tk.Label(self.StocksList.frame, text="----------------------------------")
            split.pack(padx=10, pady=3)       

        # Update the scroll region after adding new widgets
        self.StocksList.update_scrollregion()
        self.Reset()
        
    def Add_Customer(self):
        if self.admin:
            try:
                self.db.addCustomer(self.HouseEntryText.get(),
                                self.CardEntryText.get(),
                                self.NameEntryText.get(),
                                self.DOBEntryText.get(),
                                self.NumberEntryText.get(),
                                self.NLimitEntryText.get(),
                                self.BalanceEntryText.get(),
                                self.EmailEntryText.get()
                                )
                self.CustomerList.update_treeview()
            except:
                self.Logger("UNABLE TO ADD CUSTOMER!",verbose=True)

    def Delete_Customer(self):
        if self.admin and self.UID is not None:
            try:
                self.db.getCustomerID(self.UID)
            except:
                return
            try:
                self.db.deleteCustomer(self.UID)
                self.Logger(f"Customer deleted successfully\n ID: {self.UID}",verbose=True)
                self.Reset()
            except:
                self.Logger(f"No such customer\n ID: {self.UID}",verbose=True)
            self.CustomerList.update_treeview()

    def Edit_Customer(self):
        if self.admin:
            # Check if any of the entry texts are empty
            if any(value == "" for value in [
                self.HouseEntryText.get(),
                self.CardEntryText.get(),
                self.NameEntryText.get(),
                self.DOBEntryText.get(),
                self.NumberEntryText.get(),
                self.NLimitEntryText.get(),
                self.BalanceEntryText.get(),
                self.EmailEntryText.get()
            ]):
                self.Logger("Please fill in all fields before updating \nthe customer.", verbose=True)
            else:
                try:
                    self.db.editCustomer(
                        self.UID,
                        self.HouseEntryText.get(),
                        self.CardEntryText.get(),
                        self.NameEntryText.get(),
                        self.DOBEntryText.get(),
                        self.NumberEntryText.get(),
                        self.NLimitEntryText.get(),
                        self.BalanceEntryText.get(),
                        self.EmailEntryText.get()
                    )
                    self.CustomerList.update_treeview()
                except Exception as e:
                    self.Logger(f"Unable to update customer\n ID: {self.UID}\nError: {str(e)}", verbose=True)

    def TopUP(self):
        if self.admin and self.UID:
            amount = simpledialog.askfloat("Top-Up", "Enter the top-up amount:")
            if amount is None:
                return
            if amount <= 0:
                self.Logger(f"Top-Up: Customer:  {self.UID}: {self.Name}\nAmount: {amount}\nUser: {self.user}\nFailed!")
                return
            try:
                self.db.topup(self.UID, amount)
                self.CustomerList.update_treeview()
                self.Logger(f"Top-Up: Customer:  {self.UID}: {self.Name}\nAmount: {amount}\nUser: {self.user}\nSuccess!")
            except:
                self.Logger(f"Top-Up: Customer:  {self.UID}: {self.Name}\nAmount: {amount}\nUser: {self.user}\nFailed!")
        
    def Reset(self):
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
        self.UID = None
        self.Name = None
        self.House = None
        self.Email = None
        self.Number = None
        self.limit = None
        self.Balance = None
        self.DOB = None
        self.Card = None
        self.HouseEntryText.set("")
        self.CardEntryText.set("")
        self.NameEntryText.set("")
        self.DOBEntryText.set("")
        self.NumberEntryText.set("")
        self.NLimitEntryText.set("")
        self.BalanceEntryText.set("")
        self.EmailEntryText.set("")
        
        self.top.configure(background="Black")
        if self.user:
            self.top.configure(background="Green")
            self.CustomerList.update_treeview()
            for stock in self.stocks:
                self.values[stock].set(0)

    def update_total(self):
        self.total = self.sub1 + self.sub2 + self.sub3 + self.sub5 + self.sub10 + self.sub15
        self.update_reciept()
   
    def Za2ateet1(self):
        if self.user and self.Name:
            self.B1 += 1
            t = "X   "+str(self.B1)
            self.Z1AmountLabel.configure(text=t)
            self.sub1 = self.B1 * 1
            t = "Sub-total: "+str(self.sub1)
            self.Z1SubtotalLabel.configure(text= t)
            self.update_total()
        
    def Za2ateet2(self):
        if self.user and self.Name:
            self.B2 += 1
            t = "X   "+str(self.B2)
            self.Z2AmountLabel.configure(text=t)
            self.sub2 = self.B2 * 2
            t = "Sub-total: "+str(self.sub2)
            self.Z2SubtotalLabel.configure(text= t)
            self.update_total()

    def Za2ateet3(self):
        if self.user and self.Name:
            self.B3 += 1
            t = "X   "+str(self.B3)
            self.Z3AmountLabel.configure(text=t)
            self.sub3 = self.B3 * 3
            t = "Sub-total: "+str(self.sub3)
            self.Z3SubtotalLabel.configure(text= t)
            self.update_total()
            
    def Za2ateet5(self):
        if self.user and self.Name:
            self.B5 += 1
            t = "X   "+str(self.B5)
            self.Z5AmountLabel.configure(text=t)
            self.sub5 = self.B5 * 5
            t = "Sub-total: "+str(self.sub5)
            self.Z5SubtotalLabel.configure(text= t)
            self.update_total()

    def Za2ateet10(self):
        if self.user and self.Name:
            self.B10 += 1
            t = "X   "+str(self.B10)
            self.Z10AmountLabel.configure(text=t)
            self.sub10 = self.B10 * 10
            t = "Sub-total: "+str(self.sub10)
            self.Z10SubtotalLabel.configure(text= t)
            self.update_total()

    def Za2ateet15(self):
        if self.user and self.Name:
            self.B15 += 1
            t = "X   "+str(self.B15)
            self.Z15AmountLabel.configure(text=t)
            self.sub15 = self.B15 * 15
            t = "Sub-total: "+str(self.sub15)
            self.Z15SubtotalLabel.configure(text= t)
            self.update_total()

    def Za2ateet1n(self):
        if self.user and self.Name:
            if self.B1 > 0:
                self.B1 -= 1
                t = "X   "+str(self.B1)
                self.Z1AmountLabel.configure(text=t)
                self.sub1 = self.B1 * 1
                t = "Sub-total: "+str(self.sub1)
                self.Z1SubtotalLabel.configure(text= t)
                self.update_total()

    def Za2ateet2n(self):
        if self.user and self.Name:
            if self.B2 > 0:
                self.B2 -= 1
                t = "X   "+str(self.B2)
                self.Z2AmountLabel.configure(text=t)
                self.sub2 = self.B2 * 2
                t = "Sub-total: "+str(self.sub2)
                self.Z2SubtotalLabel.configure(text= t)
                self.update_total()

    def Za2ateet3n(self):
        if self.user and self.Name:
            if self.B3 > 0:
                self.B3 -= 1
                t = "X   "+str(self.B3)
                self.Z3AmountLabel.configure(text=t)
                self.sub3 = self.B3 * 3
                t = "Sub-total: "+str(self.sub3)
                self.Z3SubtotalLabel.configure(text= t)
                self.update_total()

    def Za2ateet5n(self):
        if self.user and self.Name:
            if self.B5 > 0:
                self.B5 -= 1
                t = "X   "+str(self.B5)
                self.Z5AmountLabel.configure(text=t)
                self.sub5 = self.B5 * 5
                t = "Sub-total: "+str(self.sub5)
                self.Z5SubtotalLabel.configure(text= t)
                self.update_total()

    def Za2ateet10n(self):
        if self.user and self.Name:
            if self.B10 > 0:
                self.B10 -= 1
                t = "X   "+str(self.B10)
                self.Z10AmountLabel.configure(text=t)
                self.sub10 = self.B10 * 10
                t = "Sub-total: "+str(self.sub10)
                self.Z10SubtotalLabel.configure(text= t)
                self.update_total()

    def Za2ateet15n(self):
        if self.user and self.Name:
            if self.B15 > 0:
                self.B15 -= 1
                t = "X   "+str(self.B15)
                self.Z15AmountLabel.configure(text=t)
                self.sub15 = self.B15 * 15
                t = "Sub-total: "+str(self.sub15)
                self.Z15SubtotalLabel.configure(text= t)
                self.update_total()

    def NFClogin(self, card, admin):
        self.top.configure(background="Green")
        self.user = card
        if admin:
            self.admin = True
            self.CardEntry.configure(state="readonly")
            self.DOBEntry.configure(state="normal")
            self.BalanceEntry.configure(state="normal")
            self.NLimit.configure(state="normal")
            self.NumberEntry.configure(state="normal")
            self.EmailEntry.configure(state="normal")
            self.HouseEntry.configure(state="normal")
            self.NameEntry.configure(state="normal")
        self.Logger(f"user: {self.user} logged in!")
        self.CustomerList.update_treeview()
            
    def NFClogout(self):
        self.Logger(f"user: {self.user} logged out!")
        self.Reset()
        self.user = None
        self.admin = False
        self.CardEntry.configure(state="readonly")
        self.DOBEntry.configure(state="readonly")
        self.BalanceEntry.configure(state="readonly")
        self.NLimit.configure(state="readonly")
        self.NumberEntry.configure(state="readonly")
        self.EmailEntry.configure(state="readonly")
        self.HouseEntry.configure(state="readonly")
        self.NameEntry.configure(state="readonly")
        self.CustomerList.clear_treeview()
        self.top.configure(background="Black")
               
    def NFCRegisterCard(self, card):
        self.CardEntryText.set(card) 
        self.Card = card
        self.Logger(f"new card: {self.Card}")

    def SelectCustomer(self, customer):
        return self.db.getCustomerID(customer)

    def NFCcustomer(self, args):
        self.top.configure(background="Yellow")
        self.UID = args[0]
        self.Name = args[3]
        self.House = args[1]
        self.Email = args[8]
        self.Number = args[5]
        self.limit = args[6]
        self.Balance = args[7]
        self.DOB = args[4]
        self.Card = args[2]
            
        self.NameEntryText.set(self.Name)
        self.HouseEntryText.set(self.House)
        self.EmailEntryText.set(self.Email)  
        self.NumberEntryText.set(self.Number)
        self.NLimitEntryText.set(self.limit)
        self.BalanceEntryText.set(self.Balance)
        self.DOBEntryText.set(self.DOB)
        self.CardEntryText.set(self.Card)   
        
        self.CustomerList.select_by_card_id(self.Card)        

    def Logger(self, message, verbose=False): 
        try:
            with open('log.txt', 'a') as log_file:
                log_file.write(str(datetime.now()) + " " + message + '\n')
            if verbose:
                self.LogList.append(message)
        except Exception as e:
            pass
        
    def on_exit(self):
        self.nfc.stop()
        root.destroy()
            
if __name__ == '__main__':
    root = tk.Tk()
    _top1 = root
    _w1 = Toplevel1(_top1)
    root.protocol( 'WM_DELETE_WINDOW' , _w1.on_exit)    
    root.mainloop()

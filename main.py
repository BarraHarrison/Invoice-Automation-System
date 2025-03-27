# Invoice Automation System
# An Invoice is basically a request for payment
import os 
import subprocess
import tkinter as tk 
import datetime as dt 
from tkinter import filedialog
from tkinter import messagebox
import docx 

class InvoiceAutomation:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Invoice Automation")
        self.root.geometry("500x600")

        self.partner_label = tk.Label(self.root, text="Partner")
        self.partner_label = tk.Label(self.root, text="Partner")
        self.partner_label = tk.Label(self.root, text="Partner")
        self.partner_label = tk.Label(self.root, text="Partner")
        self.partner_label = tk.Label(self.root, text="Partner")
        self.partner_label = tk.Label(self.root, text="Partner")
        self.partner_label = tk.Label(self.root, text="Partner")
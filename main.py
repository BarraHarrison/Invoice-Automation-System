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
        self.partner_street_label = tk.Label(self.root, text="Partner Street")
        self.partner_zip_country_label = tk.Label(self.root, text="Partner ZIP Code")
        self.invoice_number_label = tk.Label(self.root, text="Invoice Number")
        self.service_description_label = tk.Label(self.root, text="Service Description")
        self.service_amount_label = tk.Label(self.root, text="Service Amount")
        self.service_single_price = tk.Label(self.root, text="Service Single Price")
        self.payment_method_label = tk.Label(self.root, text="Payment Method")

        self.payment_methods = {
            "Main Bank": {
                "Recipient": "BH Company",
                "Bank": "Bank of Ireland",
                "IBAN": "AB12 3456 7891 1234",
                "BIC": "IEI44556"
            },
            "Second Bank": {
                "Recipient": "BH Company",
                "Bank": "Bank of Scotland",
                "IBAN": "SC12 8765 7891 3451",
                "BIC": "SCI46536"
            },
            "Private Bank": {
                "Recipient": "Barra Harrison",
                "Bank": "Shinhan Bank",
                "IBAN": "DF45 9826 7712 8361",
                "BIC": "KR128426"
            }
        }
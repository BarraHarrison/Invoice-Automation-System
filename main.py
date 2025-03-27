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

        # Store labels and entries in a list of tuples
        self.fields = [
            ("Partner", "partner_entry"),
            ("Partner Street", "partner_street_entry"),
            ("Partner ZIP Code", "partner_zip_country_entry"),
            ("Invoice Number", "invoice_number_entry"),
            ("Service Description", "service_description_entry"),
            ("Service Amount", "service_amount_entry"),
            ("Service Single Price", "service_single_price_entry"),
        ]

        # Dictionary to hold Entry widgets for later access
        self.entries = {}

        # Create labels and entries dynamically
        for i, (label_text, entry_attr) in enumerate(self.fields):
            label = tk.Label(self.root, text=label_text)
            label.grid(row=i, column=0, sticky="e", padx=5, pady=5)

            entry = tk.Entry(self.root)
            entry.grid(row=i, column=1, sticky="we", padx=5, pady=5)

            setattr(self, entry_attr, entry)  # Set as instance variable
            self.entries[entry_attr] = entry

        # Payment Method Label
        self.payment_method_label = tk.Label(self.root, text="Payment Method")
        self.payment_method_label.grid(row=7, column=0, sticky="e", padx=5, pady=5)

        # Payment Method Dropdown
        self.payment_method = tk.StringVar(self.root)
        self.payment_method.set("Main Bank")  # Default value

        self.payment_method_dropdown = tk.OptionMenu(
            self.root, self.payment_method, *self.payment_methods.keys()
        )
        self.payment_method_dropdown.grid(row=7, column=1, sticky="we", padx=5, pady=5)

        # Create Invoice Button
        self.create_button = tk.Button(self.root, text="Create Invoice", command=self.create_invoice)
        self.create_button.grid(row=8, column=0, columnspan=2, pady=20)

        # Make column 1 expand to fill space
        self.root.grid_columnconfigure(1, weight=1)

        self.root.mainloop()

    def create_invoice(self):
        pass


if __name__ == "__main__":
    InvoiceAutomation()
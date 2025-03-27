import os
import subprocess
import customtkinter as ctk
import datetime as dt
import docx

class InvoiceAutomation:

    def __init__(self):
        ctk.set_appearance_mode("System")  
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
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

        # Store labels and entries
        self.fields = [
            ("Partner", "partner_entry"),
            ("Partner Street", "partner_street_entry"),
            ("Partner ZIP Code", "partner_zip_country_entry"),
            ("Invoice Number", "invoice_number_entry"),
            ("Service Description", "service_description_entry"),
            ("Service Amount", "service_amount_entry"),
            ("Service Single Price", "service_single_price_entry"),
        ]

        self.entries = {}

        for i, (label_text, entry_attr) in enumerate(self.fields):
            label = ctk.CTkLabel(self.root, text=label_text)
            label.grid(row=i, column=0, sticky="e", padx=5, pady=5)

            entry = ctk.CTkEntry(self.root)
            entry.grid(row=i, column=1, sticky="we", padx=5, pady=5)

            setattr(self, entry_attr, entry)
            self.entries[entry_attr] = entry

        # Payment Method Label
        self.payment_method_label = ctk.CTkLabel(self.root, text="Payment Method")
        self.payment_method_label.grid(row=7, column=0, sticky="e", padx=5, pady=5)

        # Payment Method Dropdown
        self.payment_method = ctk.StringVar(value="Main Bank")
        self.payment_method_dropdown = ctk.CTkOptionMenu(
            self.root,
            variable=self.payment_method,
            values=list(self.payment_methods.keys())
        )
        self.payment_method_dropdown.grid(row=7, column=1, sticky="we", padx=5, pady=5)

        # Create Invoice Button
        self.create_button = ctk.CTkButton(self.root, text="Create Invoice", command=self.create_invoice)
        self.create_button.grid(row=8, column=0, columnspan=2, pady=20)

        self.root.grid_columnconfigure(1, weight=1)
        self.root.mainloop()

    def create_invoice(self):
        pass


if __name__ == "__main__":
    InvoiceAutomation()

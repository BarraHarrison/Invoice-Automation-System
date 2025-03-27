import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout,
      QHBoxLayout, QPushButton, QComboBox, QFormLayout, QMessageBox
)

class InvoiceAutomation(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Invoice Automation")
        self.setGeometry(100, 100, 400, 500)

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

        self.entries = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        fields = [
            ("Partner", "partner_entry"),
            ("Partner Street", "partner_street_entry"),
            ("Partner ZIP Code", "partner_zip_country_entry"),
            ("Invoice Number", "invoice_number_entry"),
            ("Service Description", "service_description_entry"),
            ("Service Amount", "service_amount_entry"),
            ("Service Single Price", "service_single_price_entry"),
        ]

        for label_text, entry_key in fields:
            entry = QLineEdit()
            self.entries[entry_key] = entry
            form_layout.addRow(QLabel(label_text), entry)

        self.payment_dropdown = QComboBox()
        self.payment_dropdown.addItems(self.payment_methods.keys())
        form_layout.addRow(QLabel("Payment Method"), self.payment_dropdown)

        self.create_button = QPushButton("Create Invoice")
        self.create_button.clicked.connect(self.create_invoice)

        layout.addLayout(form_layout)
        layout.addWidget(self.create_button)
        self.setLayout(layout)


    def validate_fields(self):
        for label_text, entry_key in self.fields:
            if not self.entries[entry_key].text().strip():
                QMessageBox.warning(
                    self,
                    "Missing Information",
                    f"Please fill in the '{label_text}' field."
                )
                return False
        return True

    def handle_create_invoice(self):
        pass

    def create_invoice(self):
        print("Creating invoice with the following data:")
        for key, entry in self.entries.items():
            print(f"{key}: {entry.text()}")
        print(f"Payment Method: {self.payment_dropdown.currentText()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InvoiceAutomation()
    window.show()
    sys.exit(app.exec_())
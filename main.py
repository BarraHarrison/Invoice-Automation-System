import sys
import fitz
from datetime import datetime
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
        self.create_button.clicked.connect(self.handle_create_invoice)

        layout.addLayout(form_layout)
        layout.addWidget(self.create_button)
        self.setLayout(layout)


    def validate_fields(self):
        for label_text, entry_key in self.fields:
            entry = self.entries[entry_key]
            if not entry.text().strip():
                QMessageBox.warning(
                    self,
                    "Missing Field",
                    f"The '{label_text}' field is required."
                )
                return False
        return True

    def handle_create_invoice(self):
        if self.validate_fields():
            self.create_invoice()

    def create_invoice(self):
        current_date = datetime.today().strftime("%Y-%m-%d")

        data = {
            "partner_entry": self.entries["partner_entry"].text(),
            "partner_zip_country_entry": self.entries["partner_zip_country_entry"].text(),
            "invoice_number_entry": self.entries["invoice_number_entry"].text(),
            "service_description_entry": self.entries["service_description_entry"].text(),
            "service_amount_entry": self.entries["service_amount_entry"].text(),
            "service_single_price_entry": self.entries["service_single_price_entry"].text(),
            "payment_method": self.payment_dropdown.currentText(),
            "current_date": current_date
        }

        output_filename = f'invoice_{data["invoice_number_entry"].replace("#", "")}.pdf'
        self.generate_invoice_pdf("invoice_template.pdf", output_filename, data)

        print(f"Invoice saved as {output_filename}")
        QMessageBox.information(self, "Success", f"Invoice saved as {output_filename}")


    def generate_invoice_pdf(template_path, output_path, replacements):
        doc = fitz.open(template_path)

        for page in doc:
            for key, value in replacements.items():
                placeholder = f"{{{key}}}"
                text_instances = page.search_for(placeholder)
                for inst in text_instances:
                    page.insert_text(inst[:2], value, fontsize=11, color=(0, 0, 0))
                    page.add_redact_annot(inst, fill=(1, 1, 1))
                    page.apply_redactions()
        
        doc.save(output_path)
        doc.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InvoiceAutomation()
    window.show()
    sys.exit(app.exec_())
import sys
import fitz
import smtplib
import ssl
import os
from dotenv import load_dotenv
from datetime import datetime
from email.message import EmailMessage
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout,
      QHBoxLayout, QPushButton, QComboBox, QFormLayout, QMessageBox
)
from PyQt5.QtCore import QTimer

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

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
            ("Recipient Email", "recipient_email_entry"),
        ]

        self.entries = {}
        self.init_ui()
        self.ready_label = QLabel("")
        self.ready_label.setStyleSheet("color: green; font-weight: bold;")
        self.layout().addWidget(self.ready_label)

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

        # Extract payment method details
        selected_bank = self.payment_methods[self.payment_dropdown.currentText()]

        recipient_email = self.entries["recipient_email_entry"].text()

        try:
            quantity = float(self.entries["service_amount_entry"].text())
            unit_price = float(self.entries["service_single_price_entry"].text())
            sub_total = f"${quantity * unit_price:.2f}"
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter valid numbers for amount and price.")
            return

        # Prepare data for PDF replacement
        data = {
            "partner_entry": self.entries["partner_entry"].text(),
            "partner_zip_country_entry": self.entries["partner_zip_country_entry"].text(),
            "invoice_number_entry": self.entries["invoice_number_entry"].text(),
            "service_description_entry": self.entries["service_description_entry"].text(),
            "service_amount_entry": self.entries["service_amount_entry"].text(),
            "service_single_price_entry": self.entries["service_single_price_entry"].text(),
            "payment_method": self.payment_dropdown.currentText(),
            "current_date": current_date,
            "sub_total": sub_total,
            "bank_recipient": selected_bank["Recipient"],
            "bank_name": selected_bank["Bank"],
            "bank_iban": selected_bank["IBAN"],
            "bank_bic": selected_bank["BIC"]
        }

        output_filename = f'invoice_{data["invoice_number_entry"].replace("#", "")}.pdf'
        self.generate_invoice_pdf("bank_invoice_template.pdf", output_filename, data)

        print(f"Invoice saved as {output_filename}")
        QMessageBox.information(self, "Success", f"Invoice saved as {output_filename}")

        self.send_email_with_attachment(
            recipient_email,
            subject="Your Invoice",
            body="Attached is your invoice. Thank you!",
            attachment_path=output_filename
        )

        self.clear_form()


    def send_email_with_attachment(self, recipient_email, subject, body, attachment_path):
        sender_email = EMAIL_ADDRESS
        sender_password = EMAIL_PASSWORD

        message = EmailMessage()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        message.set_content(body)

        with open(attachment_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
            message.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL("stmp.gmail.com", 465, context=context) as server:
                server.login(sender_email, sender_password)
                server.send_message(message)
            print("Email sent successfully.")
            QMessageBox.information(self, "Email Sent", f"Invoice sent to {recipient_email}")
        except Exception as e:
            print(f"Error sending email: {e}")
            QMessageBox.warning(self, "Email Failed", "There was an error sending the email.")


    def generate_invoice_pdf(self, template_path, output_path, replacements):
        doc = fitz.open(template_path)

        for page in doc:
            for key, value in replacements.items():
                placeholder = f"{{{key}}}"
                text_instances = page.search_for(placeholder)

                for inst in text_instances:
                    # Redact the placeholder text
                    page.add_redact_annot(inst, fill=(1, 1, 1))
                page.apply_redactions()

                for inst in text_instances:
                    # Write the new value AFTER redaction is applied
                    x, y = inst.x0, inst.y0

                    if key in [
                        "invoice_number_entry",
                        "partner_entry",
                        "partner_zip_country_entry",
                        "current_date",
                        "bank_recipient",
                        "bank_name",
                        "bank_iban",
                        "bank_bic",
                        "sub_total"
                            ]:
                        y += 15
                        font_size = 14
                    else:
                        font_size = 12

                    page.insert_text(
                        (x, y),
                        value,
                        fontname="helv",  
                        fontsize=font_size,
                        color=(0, 0, 0), 
                    )

        doc.save(output_path)
        doc.close()


    def clear_form(self):
        for entry in self.entries.values():
            entry.clear()
        self.payment_dropdown.setCurrentText("Main Bank")

        self.ready_label.setText("✅ Ready for the next invoice!")

        QTimer.singleShot(3000, lambda: self.ready_label.setText(""))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InvoiceAutomation()
    window.show()
    sys.exit(app.exec_())
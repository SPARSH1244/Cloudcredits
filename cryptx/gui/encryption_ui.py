from PyQt6.QtWidgets import (
    QWidget, QLabel, QTextEdit, QLineEdit, QPushButton,
    QVBoxLayout, QMessageBox, QFileDialog, QInputDialog, QComboBox
)
from core.aes import encrypt_aes, decrypt_aes
from utils.file_handler import export_to_json, export_to_pdf
from vault.vault_manager import try_load_vault
import datetime

class EncryptionTab(QWidget):
    def __init__(self):
        super().__init__()

        self.vault = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.input_label = QLabel("Enter Text:")
        self.input_text = QTextEdit()

        self.password_label = QLabel("Enter Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.vault_load_button = QPushButton("Load Key from Vault")
        self.vault_load_button.clicked.connect(self.load_key_from_vault)

        self.encrypt_btn = QPushButton("Encrypt")
        self.encrypt_btn.clicked.connect(self.encrypt_text)

        self.decrypt_btn = QPushButton("Decrypt")
        self.decrypt_btn.clicked.connect(self.decrypt_text)

        self.output_label = QLabel("Output:")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        self.export_json_btn = QPushButton("Export as JSON")
        self.export_json_btn.clicked.connect(self.export_json)

        self.export_pdf_btn = QPushButton("Export as PDF")
        self.export_pdf_btn.clicked.connect(self.export_pdf)

        layout.addWidget(self.input_label)
        layout.addWidget(self.input_text)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.vault_load_button)
        layout.addWidget(self.encrypt_btn)
        layout.addWidget(self.decrypt_btn)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_text)
        layout.addWidget(self.export_json_btn)
        layout.addWidget(self.export_pdf_btn)

        self.setLayout(layout)

    def load_key_from_vault(self):
        master_password, ok = QInputDialog.getText(self, "Vault Access", "Enter Vault Master Password:")
        if ok and master_password:
            self.vault = try_load_vault(master_password)
            if self.vault:
                keys = self.vault.get_all_keys()
                if keys:
                    key_name, ok2 = QInputDialog.getItem(self, "Select Key", "Choose saved key:", keys, 0, False)
                    if ok2 and key_name:
                        key_value = self.vault.get_key(key_name)
                        self.password_input.setText(key_value)
                        QMessageBox.information(self, "Loaded", f"Key '{key_name}' loaded into password field.")
                    else:
                        QMessageBox.warning(self, "Cancelled", "No key selected.")
                else:
                    QMessageBox.warning(self, "Empty Vault", "No keys saved in vault.")
            else:
                QMessageBox.critical(self, "Failed", "Could not unlock vault with that password.")
        else:
            QMessageBox.warning(self, "Cancelled", "Vault loading cancelled.")

    def encrypt_text(self):
        text = self.input_text.toPlainText()
        password = self.password_input.text()
        if text and password:
            encrypted = encrypt_aes(text, password)
            self.output_text.setPlainText(encrypted)
        else:
            QMessageBox.warning(self, "Error", "Text and password required!")

    def decrypt_text(self):
        text = self.input_text.toPlainText()
        password = self.password_input.text()
        if text and password:
            decrypted = decrypt_aes(text, password)
            self.output_text.setPlainText(decrypted)
        else:
            QMessageBox.warning(self, "Error", "Encrypted text and password required!")

    def export_json(self):
        text = self.output_text.toPlainText()
        if text:
            data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "operation": "Encrypt/Decrypt Output",
                "content": text
            }
            filename, _ = QFileDialog.getSaveFileName(self, "Save JSON", "", "JSON Files (*.json)")
            if filename:
                export_to_json(data, filename)
                QMessageBox.information(self, "Exported", f"Saved to {filename}")
        else:
            QMessageBox.warning(self, "Empty", "Nothing to export!")

    def export_pdf(self):
        text = self.output_text.toPlainText()
        if text:
            data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "operation": "Encrypt/Decrypt Output",
                "content": text
            }
            filename, _ = QFileDialog.getSaveFileName(self, "Save PDF", "", "PDF Files (*.pdf)")
            if filename:
                export_to_pdf(data, filename)
                QMessageBox.information(self, "Exported", f"Saved to {filename}")
        else:
            QMessageBox.warning(self, "Empty", "Nothing to export!")

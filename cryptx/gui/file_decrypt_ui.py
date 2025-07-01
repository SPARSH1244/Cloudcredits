from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox
from core.aes import decrypt_aes

import os

class FileDecryptTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.info_label = QLabel("🔓 Select an encrypted .cryptx file to decrypt")
        layout.addWidget(self.info_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter password to decrypt file")
        layout.addWidget(self.password_input)

        self.decrypt_btn = QPushButton("📂 Select Encrypted File")
        self.decrypt_btn.clicked.connect(self.select_file)
        layout.addWidget(self.decrypt_btn)

        self.setLayout(layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select .cryptx File", filter="Encrypted Files (*.cryptx)")
        if file_path:
            self.decrypt_file(file_path)

    def decrypt_file(self, file_path):
        password = self.password_input.text()
        if not password:
            QMessageBox.warning(self, "Missing Password", "Please enter a password before decrypting.")
            return

        try:
            with open(file_path, 'r', encoding='latin1') as f:
                encrypted_data = f.read()

            decrypted = decrypt_aes(encrypted_data, password)
            new_path = file_path.replace(".cryptx", "_restored")

            with open(new_path, 'wb') as f:
                f.write(decrypted.encode('latin1'))

            QMessageBox.information(self, "Success", f"File decrypted successfully:\n{new_path}")
        except Exception as e:
            QMessageBox.critical(self, "Decryption Failed", f"An error occurred:\n{str(e)}")

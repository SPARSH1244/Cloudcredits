from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
import os
from core.aes import encrypt_aes

class FileEncryptTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.info_label = QLabel("⬇️ Drag and drop a file to encrypt (.txt, .pdf, .docx, .jpg, etc.)")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter password to encrypt file")
        layout.addWidget(self.password_input)

        self.manual_btn = QPushButton("📁 Select File to Encrypt")
        self.manual_btn.clicked.connect(self.select_file)
        layout.addWidget(self.manual_btn)

        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        for url in urls:
            file_path = url.toLocalFile()
            self.encrypt_file(file_path)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Encrypt")
        if file_path:
            self.encrypt_file(file_path)

    def encrypt_file(self, file_path):
        password = self.password_input.text()
        if not password:
            QMessageBox.warning(self, "Missing Password", "Please enter a password before encrypting.")
            return

        try:
            with open(file_path, 'rb') as f:
                data = f.read()

            encrypted = encrypt_aes(data.decode('latin1'), password)
            new_path = file_path + ".cryptx"

            with open(new_path, 'w', encoding='latin1') as f:
                f.write(encrypted)

            QMessageBox.information(self, "Success", f"File encrypted successfully:\n{new_path}")
        except Exception as e:
            QMessageBox.critical(self, "Encryption Failed", f"An error occurred:\n{str(e)}")

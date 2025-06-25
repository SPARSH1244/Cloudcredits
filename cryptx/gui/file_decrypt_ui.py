from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
import os
from core.aes import decrypt_aes

class FileDecryptTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.info_label = QLabel("⬇️ Drag and drop a `.cryptx` file to decrypt")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.info_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Enter password to decrypt file")
        layout.addWidget(self.password_input)

        self.manual_btn = QPushButton("📁 Select Encrypted File (.cryptx)")
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
            self.decrypt_file(file_path)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select .cryptx File", filter="*.cryptx")
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

            output_path = file_path.replace(".cryptx", ".decrypted.txt")
            with open(output_path, 'w', encoding='latin1') as f:
                f.write(decrypted)

            QMessageBox.information(self, "Success", f"File decrypted successfully:\n{output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Decryption Failed", f"An error occurred:\n{str(e)}")

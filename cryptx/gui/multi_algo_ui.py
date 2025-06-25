from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTextEdit, QLineEdit,
    QPushButton, QComboBox, QMessageBox
)
from core.rsa_tools import generate_rsa_keys, encrypt_rsa, decrypt_rsa
from core.fernet_tools import generate_fernet_key, encrypt_fernet, decrypt_fernet
from core.caesar import caesar_encrypt, caesar_decrypt

class MultiAlgoTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.algo_label = QLabel("Select Algorithm:")
        self.algo_select = QComboBox()
        self.algo_select.addItems(["RSA", "Fernet", "Caesar Cipher"])
        self.algo_select.currentTextChanged.connect(self.update_ui)

        self.input_label = QLabel("Text:")
        self.input_text = QTextEdit()

        self.key_label = QLabel("Key / Public Key:")
        self.key_input = QTextEdit()

        self.decrypt_label = QLabel("Private Key (for RSA Decrypt):")
        self.decrypt_key_input = QTextEdit()

        self.shift_input = QLineEdit()
        self.shift_input.setPlaceholderText("Caesar Shift (e.g. 3)")

        self.encrypt_btn = QPushButton("Encrypt")
        self.encrypt_btn.clicked.connect(self.encrypt_data)

        self.decrypt_btn = QPushButton("Decrypt")
        self.decrypt_btn.clicked.connect(self.decrypt_data)

        self.output_label = QLabel("Output:")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        self.genkey_btn = QPushButton("Generate Key (RSA/Fernet)")
        self.genkey_btn.clicked.connect(self.generate_key)

        layout.addWidget(self.algo_label)
        layout.addWidget(self.algo_select)
        layout.addWidget(self.input_label)
        layout.addWidget(self.input_text)
        layout.addWidget(self.key_label)
        layout.addWidget(self.key_input)
        layout.addWidget(self.decrypt_label)
        layout.addWidget(self.decrypt_key_input)
        layout.addWidget(self.shift_input)
        layout.addWidget(self.encrypt_btn)
        layout.addWidget(self.decrypt_btn)
        layout.addWidget(self.genkey_btn)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_text)

        self.setLayout(layout)
        self.update_ui()

    def update_ui(self):
        algo = self.algo_select.currentText()
        self.key_input.setVisible(True)
        self.decrypt_key_input.setVisible(algo == "RSA")
        self.shift_input.setVisible(algo == "Caesar Cipher")

    def generate_key(self):
        algo = self.algo_select.currentText()
        if algo == "RSA":
            pub, priv = generate_rsa_keys()
            self.key_input.setPlainText(pub)
            self.decrypt_key_input.setPlainText(priv)
        elif algo == "Fernet":
            key = generate_fernet_key()
            self.key_input.setPlainText(key)
        else:
            QMessageBox.information(self, "Caesar Cipher", "No key needed. Just input a shift value.")

    def encrypt_data(self):
        algo = self.algo_select.currentText()
        text = self.input_text.toPlainText()
        key = self.key_input.toPlainText()

        try:
            if algo == "RSA":
                result = encrypt_rsa(key, text)
            elif algo == "Fernet":
                result = encrypt_fernet(key, text)
            elif algo == "Caesar Cipher":
                shift = int(self.shift_input.text())
                result = caesar_encrypt(text, shift)
            self.output_text.setPlainText(result)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def decrypt_data(self):
        algo = self.algo_select.currentText()
        text = self.input_text.toPlainText()

        try:
            if algo == "RSA":
                priv_key = self.decrypt_key_input.toPlainText()
                result = decrypt_rsa(priv_key, text)
            elif algo == "Fernet":
                key = self.key_input.toPlainText()
                result = decrypt_fernet(key, text)
            elif algo == "Caesar Cipher":
                shift = int(self.shift_input.text())
                result = caesar_decrypt(text, shift)
            self.output_text.setPlainText(result)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

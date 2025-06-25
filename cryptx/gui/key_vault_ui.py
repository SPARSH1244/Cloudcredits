from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QListWidget, QMessageBox
from vault.vault_manager import VaultManager

class KeyVaultTab(QWidget):
    def __init__(self):
        super().__init__()
        self.vault = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.master_label = QLabel("Enter Master Password:")
        self.master_input = QLineEdit()
        self.master_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.load_button = QPushButton("Load Vault")
        self.load_button.clicked.connect(self.load_vault)

        self.keyname_label = QLabel("Key Name:")
        self.keyname_input = QLineEdit()
        self.keyvalue_label = QLabel("Key Value:")
        self.keyvalue_input = QLineEdit()
        self.add_button = QPushButton("Add Key")
        self.add_button.clicked.connect(self.add_key)

        self.key_list = QListWidget()
        self.delete_button = QPushButton("Delete Selected Key")
        self.delete_button.clicked.connect(self.delete_key)

        layout.addWidget(self.master_label)
        layout.addWidget(self.master_input)
        layout.addWidget(self.load_button)

        layout.addWidget(self.keyname_label)
        layout.addWidget(self.keyname_input)
        layout.addWidget(self.keyvalue_label)
        layout.addWidget(self.keyvalue_input)
        layout.addWidget(self.add_button)

        layout.addWidget(QLabel("Saved Keys:"))
        layout.addWidget(self.key_list)
        layout.addWidget(self.delete_button)

        self.setLayout(layout)

    def load_vault(self):
        password = self.master_input.text()
        if not password:
            QMessageBox.warning(self, "Error", "Master password required")
            return

        try:
            self.vault = VaultManager(password)
            self.refresh_keys()
            QMessageBox.information(self, "Vault Loaded", "Vault unlocked successfully")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not load vault:\n{str(e)}")

    def refresh_keys(self):
        if self.vault:
            self.key_list.clear()
            keys = self.vault.get_all_keys()
            self.key_list.addItems(keys)

    def add_key(self):
        if not self.vault:
            QMessageBox.warning(self, "Error", "Load vault first")
            return

        name = self.keyname_input.text()
        value = self.keyvalue_input.text()
        if name and value:
            success = self.vault.add_key(name, value)
            if success:
                QMessageBox.information(self, "Success", f"Key '{name}' added")
                self.refresh_keys()
            else:
                QMessageBox.warning(self, "Duplicate", f"Key '{name}' already exists")
        else:
            QMessageBox.warning(self, "Error", "Both key name and value required")

    def delete_key(self):
        if not self.vault:
            QMessageBox.warning(self, "Error", "Load vault first")
            return

        selected = self.key_list.currentItem()
        if selected:
            name = selected.text()
            self.vault.delete_key(name)
            self.refresh_keys()
            QMessageBox.information(self, "Deleted", f"Key '{name}' removed")

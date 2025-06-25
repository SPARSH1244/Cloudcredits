from gui.file_decrypt_ui import FileDecryptTab
from gui.recommender_ui import RecommenderTab
from gui.key_vault_ui import KeyVaultTab
from PyQt6.QtWidgets import QMainWindow, QTabWidget
from gui.encryption_ui import EncryptionTab
from gui.password_checker import PasswordCheckerTab
from gui.multi_algo_ui import MultiAlgoTab
from gui.file_encrypt_ui import FileEncryptTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CryptX – Advanced Text Encryption Suite")
        self.setFixedSize(800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.encryption_tab = EncryptionTab()
        self.password_tab = PasswordCheckerTab()
        self.vault_tab = KeyVaultTab()
        self.recommender_tab = RecommenderTab()

        self.tabs.addTab(self.encryption_tab, "Text Encryption")
        self.tabs.addTab(self.password_tab, "Password Strength")
        self.tabs.addTab(self.vault_tab, "Key Vault")
        self.tabs.addTab(self.recommender_tab, "Smart Recommender")
        self.multi_algo_tab = MultiAlgoTab()
        self.tabs.addTab(self.multi_algo_tab, "Multi-Algorithm Lab")
        self.tabs.addTab(FileEncryptTab(), "📂 File Encryptor")
        self.tabs.addTab(FileDecryptTab(), "🔓 File Decryptor")





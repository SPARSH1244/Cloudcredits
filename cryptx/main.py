import sys
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow

def apply_dark_theme(app):
    with open("styles/dark_theme.qss", "r") as f:
        style = f.read()
        app.setStyleSheet(style)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_dark_theme(app)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

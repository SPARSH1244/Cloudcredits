from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout
from ai.strength_predictor import predict_strength

class PasswordCheckerTab(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.label = QLabel("Enter a password to analyze:")
        self.input = QLineEdit()
        self.input.textChanged.connect(self.check_password)

        self.strength_label = QLabel("")
        self.suggestion_label = QLabel("")

        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.strength_label)
        layout.addWidget(self.suggestion_label)

        self.setLayout(layout)

    def check_password(self):
        password = self.input.text()
        if password:
            level, suggestion = predict_strength(password)
            self.strength_label.setText(f"Strength: {level}")
            self.suggestion_label.setText(f"Suggestion: {suggestion}")
        else:
            self.strength_label.setText("")
            self.suggestion_label.setText("")

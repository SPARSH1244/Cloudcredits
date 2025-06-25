from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QComboBox, QTextEdit,
    QPushButton, QCheckBox
)
from core.recommender import recommend_algorithm

class RecommenderTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.purpose_label = QLabel("Purpose:")
        self.purpose_input = QComboBox()
        self.purpose_input.addItems(["Personal", "Sharing", "Demo/Learning", "Confidential"])

        self.keytype_label = QLabel("Key Type:")
        self.keytype_input = QComboBox()
        self.keytype_input.addItems(["Symmetric", "Asymmetric"])

        self.speed_checkbox = QCheckBox("Prioritize Speed?")

        self.text_label = QLabel("Sample Text:")
        self.text_input = QTextEdit()

        self.recommend_button = QPushButton("Recommend Best Algorithm")
        self.recommend_button.clicked.connect(self.recommend_algo)

        self.result_label = QLabel("Recommended Algorithm: ")

        layout.addWidget(self.purpose_label)
        layout.addWidget(self.purpose_input)
        layout.addWidget(self.keytype_label)
        layout.addWidget(self.keytype_input)
        layout.addWidget(self.speed_checkbox)
        layout.addWidget(self.text_label)
        layout.addWidget(self.text_input)
        layout.addWidget(self.recommend_button)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def recommend_algo(self):
        text = self.text_input.toPlainText()
        purpose = self.purpose_input.currentText()
        key_type = self.keytype_input.currentText().lower()
        speed = self.speed_checkbox.isChecked()

        result = recommend_algorithm(
            text=text,
            purpose=purpose,
            speed_priority=speed,
            key_type=key_type
        )
        self.result_label.setText(f"Recommended Algorithm: {result}")

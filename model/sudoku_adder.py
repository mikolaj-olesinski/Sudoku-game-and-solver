import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

class AddSudokuWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dodaj Sudoku")
        self.setGeometry(100, 100, 300, 150)

        self.option_label = QLabel("Wybierz sposób dodania sudoku:")
        self.option_combo_box = QComboBox()
        self.option_combo_box.addItems(["Opcja 1", "Opcja 2", "Opcja 3"])  # Dodaj tutaj swoje opcje

        self.add_button = QPushButton("Dodaj")
        self.add_button.setObjectName("add_button")

        layout = QVBoxLayout()
        layout.addWidget(self.option_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.option_combo_box)
        layout.addWidget(self.add_button, alignment=Qt.AlignCenter)

        layout.setContentsMargins(20, 20, 20, 20)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)


from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QLabel, QComboBox, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

class AddSudokuGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dodaj Sudoku")
        self.setGeometry(100, 100, 300, 150)

        self.option_label = QLabel("Wybierz sposób dodania sudoku:")
        self.option_combo_box = QComboBox()
        self.option_combo_box.addItems(["Dodaj z pliku", "Stwórz własny", "Dodaj ze zdjecia"]) 

        self.go_back_button = QPushButton("Cofnij")
        self.go_back_button.setObjectName("go_back_button")

        self.add_button = QPushButton("Dodaj")
        self.add_button.setObjectName("add_button")

        layout = QVBoxLayout()
        layout.addWidget(self.option_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.option_combo_box)

        layout_for_buttons = QHBoxLayout()
        layout_for_buttons.addWidget(self.go_back_button)
        layout_for_buttons.addWidget(self.add_button)
        layout_for_buttons.setContentsMargins(0, 12, 0, 0)


        layout.addLayout(layout_for_buttons)
        layout.setContentsMargins(20, 20, 20, 20)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)



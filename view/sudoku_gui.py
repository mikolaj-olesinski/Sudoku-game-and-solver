from PySide6.QtWidgets import QWidget,QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from model.utils.classes import Stoper
from model.sudoku_class import Sudoku as SudokuWidget

class TopWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        cofniecie = QPushButton("Cofnij")
        stoper = Stoper()

        layout.addWidget(cofniecie)
        layout.addWidget(stoper)

        self.stoper = stoper
        self.cofniecie = cofniecie

class BottomWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        save_button = QPushButton("Zapisz")
        save_button.setObjectName("save_button")

        hint_button = QPushButton("Podpowiedz")
        hint_button.setObjectName("hint_button")

        layout.addWidget(save_button)
        layout.addWidget(hint_button)

        self.hint_button = hint_button
        self.save_button = save_button


class SudokuGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        self.top_widget = TopWidget()
        self.sudoku = SudokuWidget()
        self.bottom_widget = BottomWidget()

        main_layout.addWidget(self.top_widget)
        main_layout.addWidget(self.sudoku)
        main_layout.addWidget(self.bottom_widget)

        self.setLayout(main_layout)
        self.setWindowTitle('Sudoku Application')
        self.setGeometry(100, 100, 700, 600)

import sys
from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QFrame, QVBoxLayout, QLabel, QPushButton, QMessageBox, QHBoxLayout
from PySide6.QtCore import Qt, QTimer
from nwm import NonZeroValidator, UserCell, ComputerCell, BlankCell, Stoper
from datetime import datetime
from sudoku_square import SudokuSquare
from sudoku_class import Sudoku as SudokuWidget

class TopWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(QLabel("Cofniecie"))
        layout.addWidget(QLabel("Score"))
        layout.addWidget(Stoper())




class BottomWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.addWidget(QPushButton("Zapisz"))
        layout.addWidget(QPushButton("Podpowiedz"))


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




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = SudokuGUI()
    main_window.show()
    sys.exit(app.exec())

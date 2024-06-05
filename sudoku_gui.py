import sys
from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QFrame, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from nwm import NonZeroValidator, UserCell, ComputerCell, BlankCell
from datetime import datetime

from sudoku_square import SudokuSquare
from sudoku_class import Sudoku as SudokuWidget

class TopWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(QLabel("Top Section"))
        # Dodaj tutaj inne widgety według potrzeb


class BottomWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(QLabel("Bottom Section"))
        self.popup_button = QPushButton('Show Popup')
        self.popup_button.clicked.connect(self.show_popup)
        layout.addWidget(self.popup_button)
        # Dodaj tutaj inne widgety według potrzeb

    def show_popup(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("This is a popup message.")
        msg.setInformativeText("Additional information can go here.")
        msg.setWindowTitle("Popup")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        retval = msg.exec()


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

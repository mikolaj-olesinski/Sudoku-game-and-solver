import sys
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QFrame
from PySide6.QtCore import Qt
from nwm import NonZeroValidator

class SudokuSquare(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        layout = QGridLayout()
        self.setLayout(layout)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
    

        self.cells = []

        for row in range(3):
            row_cells = []
            for col in range(3):
                cell = QLineEdit()
                cell.setAlignment(Qt.AlignCenter)
                cell.setFixedSize(80, 80)  # Ustawienie stałego rozmiaru komórki
                cell.setValidator(NonZeroValidator())
                cell.setMaxLength(1)
                layout.addWidget(cell, row, col)
                row_cells.append(cell)
            self.cells.append(row_cells)

    def validate_square(self, x, y):
        numbers = []
        for i in range(3):
            for j in range(3):
                cell = self.cells[i][j]

                if cell.text():
                    numbers.append(cell.text())
        if len(numbers) != len(set(numbers)):
            return False
        return True
    
    def print_objects_on_square(self):
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                print(cell)

from PySide6.QtWidgets import QWidget, QGridLayout, QLineEdit
from PySide6.QtCore import Qt
from model.utils.classes import NonZeroValidator

class SudokuSquare(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        layout = QGridLayout()
        self.setLayout(layout)
        layout.setSpacing(0)
    

        self.cells = []

        for row in range(3):
            row_cells = []
            for col in range(3):
                cell = QLineEdit()
                cell.setAlignment(Qt.AlignCenter)
                cell.setFixedSize(80, 80)
                cell.setValidator(NonZeroValidator())
                cell.setMaxLength(1)
                layout.addWidget(cell, row, col)
                layout.setContentsMargins(0, 0, 0, 0)
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
    
    def check_square_for_win(self):
        numbers = []
        for i in range(3):
            for j in range(3):
                cell = self.cells[i][j]

                if cell.text():
                    numbers.append(cell.text())
        if len(set(numbers)) == 9:
            return True
        return False
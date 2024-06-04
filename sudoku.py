import sys
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QFrame
from PySide6.QtCore import Qt
from nwm import NonZeroValidator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dataBase.models import Sudoku, User, UsersSudoku, Base

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

class Sudoku(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.setObjectNames()
        self.cells = self.findCells()
        self.squares = self.findSquares()


    def initUI(self):
        self.setWindowTitle('Sudoku')
        self.setGeometry(100, 100, 700, 700)

        grid = QGridLayout()
        self.setLayout(grid)

        self.squares = []

        for row in range(3):
            row_squares = []
            for col in range(3):
                square = SudokuSquare()
                grid.addWidget(square, row, col)
                row_squares.append(square)
            self.squares.append(row_squares)

    def setObjectNames(self):
        for i, row in enumerate(self.squares):
            for j, square in enumerate(row):
                square.setObjectName(f'square_{i}_{j}')
                for x, row in enumerate(square.cells):
                    for y, cell in enumerate(row):
                        cell.setObjectName(f'cell_{i * 3 + x}_{j * 3 + y}')

    def findCells(self):
        cells = {}
        for i in range(9):
            for j in range(9):
                cell_name = f'cell_{i}_{j}'
                cells[cell_name] = self.findChild(QLineEdit, cell_name)
        return cells
    
    def findSquares(self):

        squares = {}
        for i in range(3):
            for j in range(3):
                square_name = f'square_{i}_{j}'
                squares[square_name] = self.findChild(SudokuSquare, square_name)
        return squares

    def validate_row(self, row):
        numbers = []
        for i in range(9):
            cell = self.cells[f'cell_{row}_{i}']
            if cell.text():
                numbers.append(cell.text())
            
        if len(numbers) != len(set(numbers)):
            return False
        return True

    def validate_column(self, column):
        numbers = []
        for i in range(9):
            cell = self.cells[f'cell_{i}_{column}']
            if cell.text():
                numbers.append(cell.text())
        
        if len(numbers) != len(set(numbers)):
            return False
        return True
    

    def update_board(self, board):
        for cell_name, value in board.items():
            cell = self.cells[cell_name]
            
            if value != '0':
                if value[0] == 'C':
                    cell.setText(value[1])
                    cell.setFocusPolicy(Qt.NoFocus)
                    cell.setStyleSheet('color: white')
                elif value[0] == 'U':
                    cell.setText(value[1])
            
            else:
                cell.setText('')

            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Sudoku()
    ex.get_board_from_file('sudoku.txt')
    ex.show()
    sys.exit(app.exec())

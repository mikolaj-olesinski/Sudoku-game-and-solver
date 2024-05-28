from sudoku import Sudoku, SudokuSquare
import sys
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QFrame
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt



def display_cell_text(cell):
    print(cell.objectName())

def validate_cell_changed_text(cell):
    cell_row = int(cell.objectName()[5])
    cell_col = int(cell.objectName()[7])

    square_row = cell_row // 3
    square_col = cell_col // 3

    square = window.squares[f'square_{square_row}_{square_col}']

    if not square.validate_square(cell_row, cell_col) or not window.validate_column(cell_col) or not window.validate_row(cell_row):
        cell.setStyleSheet('background-color: red')
        return False
    else:
        cell.setStyleSheet('background-color: dark grey')
        return True


    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    sudoku = Sudoku()
    sudoku.update_board('sudoku.txt')
    sudoku.setStyleSheet(open('style.qss').read())
    window = sudoku
    window.show()



    cells = sudoku.cells
    for cell in cells:
        cells[cell].editingFinished.connect(lambda cell=cell: validate_cell_changed_text(cells[cell]))


    sys.exit(app.exec())


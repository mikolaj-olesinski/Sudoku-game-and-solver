from sudoku_class import Sudoku 
import sys
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QFrame
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import Qt
from nwm import get_board_from_db, get_board_from_file, UserCell, ComputerCell, BlankCell, NonZeroValidator
from sudoku_gui import SudokuGUI


def display_cell_text(cell):
    print(cell)


def validate_cell_changed_text(cell, sudoku):
    cell_row = int(cell.objectName().split('_')[1])
    cell_col = int(cell.objectName().split('_')[2])

    square_row = cell_row // 3
    square_col = cell_col // 3

    square = sudoku.squares[f'square_{square_row}_{square_col}']
    if not square.validate_square(cell_row, cell_col) or not sudoku.validate_column(cell_col) or not sudoku.validate_row(cell_row):
        cell.setStyleSheet('color: #b56')
        return False
    else:
        if not isinstance(cell, ComputerCell):

            cell.setStyleSheet('color: #458;')

        return True

    
if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = SudokuGUI()

    sudoku = main_window.sudoku
    sudoku.update_board(get_board_from_db(1))
    app.setStyleSheet(open('style.qss').read())


    cells = sudoku.cells
    for cell_name, cell in cells.items():
        cell.editingFinished.connect(lambda cell=cell: validate_cell_changed_text(cell, sudoku))

    main_window.show()

    sys.exit(app.exec())




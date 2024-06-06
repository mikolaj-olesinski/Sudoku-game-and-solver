import sys
from PySide6.QtWidgets import QApplication
from model.utils.func import get_board_from_db, get_board_from_file
from view.sudoku_gui import SudokuGUI
from controller.sudoku_control import validate_cell_changed_text

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    main_window = SudokuGUI()

    sudoku = main_window.sudoku
    sudoku.update_board(get_board_from_db(1))
    #sudoku.update_board(get_board_from_file('constants/sudoku.txt'))
    app.setStyleSheet(open('view/style.qss').read())


    cells = sudoku.cells
    for cell_name, cell in cells.items():
        cell.editingFinished.connect(lambda cell=cell: validate_cell_changed_text(cell, sudoku))

    main_window.show()

    sys.exit(app.exec())




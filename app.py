import sys
from PySide6.QtWidgets import QApplication, QPushButton
from model.utils.func import get_board_from_db, get_board_from_file
from view.sudoku_gui import SudokuGUI
from controller.sudoku_control import validate_cell_changed_text, hint_for_sudoku

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    main_window = SudokuGUI()

    sudoku = main_window.sudoku
    sudoku.update_board(get_board_from_db(1)[0], get_board_from_db(1)[1])
    #sudoku.update_board(get_board_from_file('constants/sudoku.txt'))
    app.setStyleSheet(open('view/style.qss').read())


    cells = sudoku.cells
    for cell_name, cell in cells.items():
        row, col = int(cell_name.split('_')[1]), int(cell_name.split('_')[2])
        cell.editingFinished.connect(lambda cell=cell: validate_cell_changed_text(cell, sudoku))
        cell.returnPressed.connect(lambda cell=cell, row=row, col=col: hint_for_sudoku(sudoku, row, col))

    hint_button = main_window.bottom_widget.findChild(QPushButton, 'hint_button')
    hint_button.clicked.connect(lambda: hint_for_sudoku(sudoku))

    main_window.show()

    sys.exit(app.exec())




from PySide6.QtWidgets import QPushButton, QDialog
from model.utils.func import get_board_from_db
from view.sudoku_gui import SudokuGUI
from controller.controls.sudoku_control import validate_cell_changed_text, hint_for_sudoku, save_sudoku
from model.utils.classes import BlankCell

class sudoku_app(SudokuGUI):

    def __init__(self):
        super().__init__()
        sudoku = self.sudoku
        sudoku.update_board(get_board_from_db(1)[0], get_board_from_db(1)[1])
        cells = sudoku.cells
        for cell_name, cell in cells.items():
            row, col = int(cell_name.split('_')[1]), int(cell_name.split('_')[2])

            if isinstance(cell, BlankCell):
                cell.returnPressed.connect(lambda cell=cell, row=row, col=col: hint_for_sudoku(sudoku, row, col))
                cell.editingFinished.connect(lambda cell=cell: validate_cell_changed_text(cell, sudoku))

        hint_button = self.findChild(QPushButton, 'hint_button')
        hint_button.clicked.connect(lambda: hint_for_sudoku(sudoku))
        #zmienic to na gorze i na dole potem to ma swoje atrybuty
        save_button = self.findChild(QPushButton, 'save_button')
        save_button.clicked.connect(lambda: save_sudoku(sudoku))


from model.utils.func import get_data_from_sudoku, is_solvable, get_board_from_string
from view.sudoku_creator_gui import SudokuCreatorGUI
from controller.controls.sudoku_control import validate_cell_changed_text
from database.addData import addSudoku
from PySide6.QtWidgets import QMessageBox

class SudokuCreatorApp(SudokuCreatorGUI):
    def __init__(self, sudoku_picker_app, data=None):
        super().__init__()
        self.sudoku_picker_app = sudoku_picker_app
        if data:
            self.sudoku.update_board(get_board_from_string(data), blank_cell_color='white')


        self._connect_cells(self.sudoku.cells)
        self._connect_buttons()

    def _connect_cells(self, cells):
        for _, cell in cells.items():
            cell.editingFinished.connect(lambda cell=cell: validate_cell_changed_text(cell, self.sudoku, color='white'))
            


    def _connect_buttons(self):
        save_button = self.bottom_widget.save_button
        back_button = self.top_widget.cofniecie

        save_button.clicked.connect(self._handle_save_button)
        back_button.clicked.connect(self._handle_back_button)


    def _handle_save_button(self):
        if is_solvable(get_data_from_sudoku(self.sudoku)):
            QMessageBox.about(self, 'Sudoku dodane', 'Sudoku zostało dodane do bazy danych.')
            addSudoku(get_data_from_sudoku(self.sudoku))
            self.sudoku_picker_app.sudoku_picker.update_data()
            self._handle_back_button()
        else:
            QMessageBox.about(self, 'Sudoku nie jest rozwiązalne', 'Sudoku nie jest rozwiązalne. Proszę poprawić sudoku.')
    
    def _handle_back_button(self): 
        self.sudoku_picker_app.show()
        self.close()

        



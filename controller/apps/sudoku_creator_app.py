from model.utils.func import get_data_from_sudoku
from view.sudoku_creator_gui import SudokuCreatorGUI
from controller.controls.sudoku_control import validate_cell_changed_text_for_creator
from model.utils.classes import BlankCell
from database.addData import addSudoku

class SudokuCreatorApp(SudokuCreatorGUI):
    def __init__(self, sudoku_picker_app):
        super().__init__()
        self.sudoku_picker_app = sudoku_picker_app

        self._connect_cells(self.sudoku.cells)
        self._connect_buttons()

    def _connect_cells(self, cells):
        for cell_name, cell in cells.items():
            cell.editingFinished.connect(lambda cell=cell: validate_cell_changed_text_for_creator(cell, self.sudoku))
            


    def _connect_buttons(self):
        save_button = self.bottom_widget.save_button
        back_button = self.top_widget.cofniecie


        save_button.clicked.connect(self._handle_save_button)
        back_button.clicked.connect(self._handle_back_button)


    def _handle_save_button(self):
        print(get_data_from_sudoku(self.sudoku))
        addSudoku(get_data_from_sudoku(self.sudoku))
        self.sudoku_picker_app.sudoku_picker.update_data()
        self._handle_back_button()
    
    def _handle_back_button(self): 
        self.sudoku_picker_app.show()
        self.close()

        



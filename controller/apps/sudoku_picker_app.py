from model.utils.func import get_board_from_db
from view.sudoku_picker_gui import SudokuPickerGUI
from controller.controls.sudoku_control import validate_cell_changed_text, hint_for_sudoku, save_sudoku, check_sudoku_for_win
from model.utils.classes import BlankCell
from database.getData import get_timer
from database.addData import addTimer
from model.sudoku_adder import AddSudokuWindow

class sudoku_picker_app(SudokuPickerGUI):
    def __init__(self, user_id, login_app):
        super().__init__(user_id)
        self.login_app = login_app
        self.connect_back_button()
        self.connect_add_sudoku_button()
    
    def connect_back_button(self):
        self.top_widget.cofniecie.clicked.connect(self._handle_back_button)

    def connect_add_sudoku_button(self):
        self.bottom_widget.add_sudoku_button.clicked.connect(self._handle_add_sudoku_button)

    def _handle_back_button(self):
        self.login_app.show()
        self.close()

    def _handle_add_sudoku_button(self):
        self.add_sudoku_window = AddSudokuWindow()
        self.add_sudoku_window.show()
        self.close()

    
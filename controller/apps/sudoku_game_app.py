from model.utils.func import get_board_from_db
from view.sudoku_game_gui import SudokuGUI, TopWidget
from controller.controls.sudoku_control import validate_cell_changed_text, hint_for_sudoku, save_sudoku, check_sudoku_for_win
from model.utils.classes import BlankCell
from database.getData import get_timer
from database.addData import addTimer

class sudoku_app(SudokuGUI):
    def __init__(self, user_id, sudoku_id, sudoku_picker):
        super().__init__()
        self.sudoku.user_id = user_id
        self.sudoku_id = sudoku_id
        self.sudoku_picker = sudoku_picker

        self.sudoku.update_board(get_board_from_db(sudoku_id, user_id), sudoku_id)
        self._update_time()

        self._connect_cells(self.sudoku.cells)
        self._connect_buttons()

    def _connect_cells(self, cells):
        for cell_name, cell in cells.items():
            row, col = self._extract_row_col(cell_name)

            if isinstance(cell, BlankCell):
                cell.returnPressed.connect(lambda cell=cell, row=row, col=col: hint_for_sudoku(self.sudoku, row, col))
                cell.editingFinished.connect(lambda cell=cell: validate_cell_changed_text(cell, self.sudoku))
                cell.editingFinished.connect(lambda: check_sudoku_for_win(self))
            


    def _extract_row_col(self, cell_name):
        parts = cell_name.split('_')
        return int(parts[1]), int(parts[2])

    def _connect_buttons(self):
        hint_button = self.bottom_widget.hint_button
        save_button = self.bottom_widget.save_button
        back_button = self.top_widget.cofniecie

        hint_button.clicked.connect(self._handle_hint_button)
        save_button.clicked.connect(self._handle_save_button)
        back_button.clicked.connect(self._handle_back_button)

    def _handle_hint_button(self):
        hint_for_sudoku(self.sudoku)
        check_sudoku_for_win(self)

    def _handle_save_button(self):
        save_sudoku(self.sudoku)
        self._save_time()
    
    def _handle_back_button(self): 
        self._handle_save_button()
        self.sudoku_picker.update_data()
        self.sudoku_picker.show()
        self.close()

        
    def _update_time(self):
        self.top_widget.stoper.set_time(get_timer(self.sudoku.user_id, self.sudoku.id))
    
    def _save_time(self):
        time = self.top_widget.stoper.get_time()
        addTimer(self.sudoku.user_id, self.sudoku.id, time)



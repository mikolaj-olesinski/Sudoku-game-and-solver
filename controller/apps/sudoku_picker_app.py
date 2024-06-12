from view.sudoku_picker_gui import SudokuPickerGUI
from controller.apps.sudoku_adder_app import SudokuAdderApp

class sudoku_picker_app(SudokuPickerGUI):
    def __init__(self, user_id, login_app):
        super().__init__(user_id)
        self.login_app = login_app
        self.sudoku_picker.app = self
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
        self.add_sudoku_window = SudokuAdderApp(self)
        self.add_sudoku_window.show()
        self.close()

    
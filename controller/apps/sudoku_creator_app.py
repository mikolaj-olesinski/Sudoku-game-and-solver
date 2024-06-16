from model.utils.func import get_data_from_sudoku, is_solvable, get_board_from_string
from view.sudoku_creator_gui import SudokuCreatorGUI
from controller.controls.sudoku_control import validate_cell_changed_text
from database.addData import addSudoku
from PySide6.QtWidgets import QMessageBox

class  SudokuCreatorApp(SudokuCreatorGUI):
    """
    The SudokuCreatorApp class provides functionality for creating and validating Sudoku puzzles.
    It allows users to input Sudoku puzzles manually and save them to a database if they are solvable.

    Methods
    -------
    __init__(sudoku_picker_app, data=None):
        Initializes the SudokuCreatorApp instance and sets up the Sudoku board if data is provided.
    
    _connect_cells(cells):
        Connects each cell's editingFinished signal to the validation function.

    _connect_buttons():
        Connects the save and back buttons to their respective handlers.
    
    _handle_save_button():
        Handles the event when the save button is clicked, checking if the Sudoku puzzle is solvable and saving it to the database.

    _handle_back_button():
        Handles the event when the back button is clicked, showing the Sudoku picker app and closing the current window.
    """

    def __init__(self, sudoku_picker_app, data=None):
        """
        Initializes the SudokuCreatorApp instance. This method sets up the 
        initial state of the application, connects cells and buttons to their 
        respective handlers, and optionally sets up the Sudoku board with provided data.

        Parameters
        ----------
        sudoku_picker_app : QApplication
            The main application instance that handles the Sudoku picker.
        data : str, optional
            A string representing a Sudoku puzzle to initialize the board with (default is None).
        """
        super().__init__()
        self.sudoku_picker_app = sudoku_picker_app
        if data:
            self.sudoku.update_board(get_board_from_string(data), blank_cell_color='white')

        self._connect_cells(self.sudoku.cells)
        self._connect_buttons()

    def _connect_cells(self, cells):
        """
        Connects each cell's editingFinished signal to the validate_cell_changed_text function.

        Parameters
        ----------
        cells : dict
            A dictionary of cell widgets in the Sudoku board.
        """
        for _, cell in cells.items():
            cell.editingFinished.connect(lambda cell=cell: validate_cell_changed_text(cell, self.sudoku, color='white'))

    def _connect_buttons(self):
        """Connects the save and back buttons to their respective handler methods."""
        save_button = self.bottom_widget.save_button
        back_button = self.top_widget.cofniecie

        save_button.clicked.connect(self._handle_save_button)
        back_button.clicked.connect(self._handle_back_button)

    def _handle_save_button(self):
        """
        Handles the event when the save button is clicked. This method checks if the Sudoku puzzle
        is solvable, saves it to the database, updates the Sudoku picker, and shows a message to the user.
        """
        if is_solvable(get_data_from_sudoku(self.sudoku)):
            QMessageBox.about(self, 'Sudoku dodane', 'Sudoku zostało dodane do bazy danych.')
            addSudoku(get_data_from_sudoku(self.sudoku))
            self.sudoku_picker_app.sudoku_picker.update_data()
            self._handle_back_button()
        else:
            QMessageBox.about(self, 'Sudoku nie jest rozwiązalne', 'Sudoku nie jest rozwiązalne. Proszę poprawić sudoku.')
    
    def _handle_back_button(self): 
        """Handles the event when the back button is clicked, showing the Sudoku picker app and closing the current window."""
        self.sudoku_picker_app.show()
        self.close()

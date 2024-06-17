from model.utils.func import get_board_from_db
from view.sudoku_game_gui import SudokuGUI
from controller.controls.sudoku_control import validate_cell_changed_text, hint_for_sudoku, save_sudoku, check_sudoku_for_win, isFull
from model.utils.classes import BlankCell
from database.getData import get_timer
from database.addData import addTimer

class sudoku_app(SudokuGUI):
    """
    The sudoku_app class provides functionality for playing a Sudoku game.
    It initializes the game board, connects cell and button events, and manages the game state.

    Methods
    -------
    __init__(user_id, sudoku_id, sudoku_picker):
        Initializes the sudoku_app instance and sets up the game board with data from the database.
    
    _connect_cells(cells):
        Connects each cell's signals to the appropriate validation and hint functions.

    _extract_row_col(cell_name):
        Extracts the row and column indices from a cell's name.

    _connect_buttons():
        Connects the hint, save, and back buttons to their respective handlers.
    
    _handle_hint_button():
        Handles the event when the hint button is clicked, providing a hint for the Sudoku puzzle.

    _handle_save_button():
        Handles the event when the save button is clicked, saving the current state of the Sudoku puzzle.

    _handle_back_button():
        Handles the event when the back button is clicked, saving the current state and navigating back to the Sudoku picker.
    
    _update_time():
        Updates the timer with the saved time from the database.

    _save_time():
        Saves the current time to the database.
    """

    def __init__(self, user_id, sudoku_id, sudoku_picker):
        """
        Initializes the sudoku_app instance. This method sets up the initial state of the application,
        connects cells and buttons to their respective handlers, and updates the timer.

        Parameters
        ----------
        user_id : int
            The ID of the current user.
        sudoku_id : int
            The ID of the current Sudoku puzzle.
        sudoku_picker : QApplication
            The main application instance that handles the Sudoku picker.
        """
        super().__init__()
        self.sudoku.user_id = user_id
        self.sudoku_id = sudoku_id
        self.sudoku_picker = sudoku_picker

        self.sudoku.update_board(get_board_from_db(sudoku_id, user_id), sudoku_id)
        self._update_time()

        self._connect_cells(self.sudoku.cells)
        self._connect_buttons()

    def _connect_cells(self, cells):
        """
        Connects each cell's signals to the appropriate validation and hint functions.

        Parameters
        ----------
        cells : dict
            A dictionary of cell widgets in the Sudoku board.
        """
        for cell_name, cell in cells.items():
            row, col = self._extract_row_col(cell_name)

            if isinstance(cell, BlankCell):
                cell.returnPressed.connect(lambda cell=cell, row=row, col=col: hint_for_sudoku(self.sudoku, row, col))
                cell.editingFinished.connect(lambda cell=cell: validate_cell_changed_text(cell, self.sudoku))
                cell.editingFinished.connect(lambda: check_sudoku_for_win(self))

    def _extract_row_col(self, cell_name):
        """
        Extracts the row and column indices from a cell's name.

        Parameters
        ----------
        cell_name : str
            The name of the cell in the format 'cell_row_col'.

        Returns
        -------
        tuple
            A tuple containing the row and column indices.
        """
        parts = cell_name.split('_')
        return int(parts[1]), int(parts[2])

    def _connect_buttons(self):
        """Connects the hint, save, and back buttons to their respective handler methods."""
        hint_button = self.bottom_widget.hint_button
        save_button = self.bottom_widget.save_button
        back_button = self.top_widget.cofniecie

        hint_button.clicked.connect(self._handle_hint_button)
        save_button.clicked.connect(self._handle_save_button)
        back_button.clicked.connect(self._handle_back_button)

    def _handle_hint_button(self):
        """
        Handles the event when the hint button is clicked. This method provides a hint
        for the Sudoku puzzle and checks if the puzzle is solved.
        """
        if isFull(self.sudoku):
            return
        hint_for_sudoku(self.sudoku)
        check_sudoku_for_win(self)

    def _handle_save_button(self):
        """
        Handles the event when the save button is clicked. This method saves the current
        state of the Sudoku puzzle and the timer.
        """
        save_sudoku(self.sudoku)
        self._save_time()
    
    def _handle_back_button(self): 
        """
        Handles the event when the back button is clicked. This method saves the current
        state of the Sudoku puzzle, updates the Sudoku picker, and navigates back to the Sudoku picker.
        """
        self._handle_save_button()
        self.sudoku_picker.update_data()
        self.sudoku_picker.app.show()
        self.close()

    def _update_time(self):
        """Updates the timer with the saved time from the database."""
        self.top_widget.stoper.set_time(get_timer(self.sudoku.user_id, self.sudoku.id))
    
    def _save_time(self):
        """Saves the current time to the database."""
        time = self.top_widget.stoper.get_time()
        addTimer(self.sudoku.user_id, self.sudoku.id, time)

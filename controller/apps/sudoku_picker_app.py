from view.sudoku_picker_gui import SudokuPickerGUI
from controller.apps.sudoku_adder_app import SudokuAdderApp

class sudoku_picker_app(SudokuPickerGUI):
    """
    The sudoku_picker_app class provides functionality for picking a Sudoku puzzle.
    It allows users to navigate back to the login screen or add a new Sudoku puzzle.

    Methods
    -------
    __init__(user_id, login_app):
        Initializes the sudoku_picker_app instance and sets up the Sudoku picker interface.
    
    connect_back_button():
        Connects the back button to its handler.

    connect_add_sudoku_button():
        Connects the add Sudoku button to its handler.
    
    _handle_back_button():
        Handles the event when the back button is clicked, showing the login screen.

    _handle_add_sudoku_button():
        Handles the event when the add Sudoku button is clicked, opening the Sudoku adder window.
    """

    def __init__(self, user_id, login_app):
        """
        Initializes the sudoku_picker_app instance. This method sets up the initial state of the application,
        connects buttons to their respective handlers, and initializes the login application.

        Parameters
        ----------
        user_id : int
            The ID of the current user.
        login_app : QApplication
            The main application instance that handles the login screen.
        """
        super().__init__(user_id)
        self.login_app = login_app
        self.sudoku_picker.app = self
        self.connect_back_button()
        self.connect_add_sudoku_button()

    def connect_back_button(self):
        """Connects the back button click event to the _handle_back_button method."""
        self.top_widget.cofniecie.clicked.connect(self._handle_back_button)

    def connect_add_sudoku_button(self):
        """Connects the add Sudoku button click event to the _handle_add_sudoku_button method."""
        self.bottom_widget.add_sudoku_button.clicked.connect(self._handle_add_sudoku_button)

    def _handle_back_button(self):
        """Handles the event when the back button is clicked, showing the login screen and closing the current window."""
        self.login_app.show()
        self.close()

    def _handle_add_sudoku_button(self):
        """
        Handles the event when the add Sudoku button is clicked. This method opens the Sudoku adder window,
        shows it, and closes the current window.
        """
        self.add_sudoku_window = SudokuAdderApp(self)
        self.add_sudoku_window.show()
        self.close()

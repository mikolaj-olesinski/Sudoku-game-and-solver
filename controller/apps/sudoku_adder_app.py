from model.utils.func import get_sudoku_string_from_file, is_valid, get_sudoku_from_api
from view.sudoku_adder_gui import AddSudokuGUI
from controller.apps.sudoku_creator_app import SudokuCreatorApp
from PySide6.QtWidgets import QMessageBox, QFileDialog
from model.PhotoDetection.sudokiMain import get_sudoku_from_image
import os
import numpy as np

class SudokuAdderApp(AddSudokuGUI):
    """
    The SudokuAdderApp class provides functionality for adding Sudoku puzzles
    through various methods such as from a file, manually created by the user, or from an image.

    Methods
    -------
    __init__(sudoku_picker_app):
        Initializes the SudokuAdderApp instance and connects UI elements to their respective handlers.
    
    _connect_add_button():
        Connects the add button to its handler.

    _connect_go_back_button():
        Connects the go back button to its handler.
    
    _handle_go_back_button():
        Handles the event when the go back button is clicked.

    _handle_add_button():
        Handles the event when the add button is clicked and determines the source of the Sudoku puzzle.
    
    addSudokuFromUser():
        Opens the Sudoku creator application for the user to manually create a Sudoku puzzle.

    addSudokuFromFile():
        Opens a file dialog for the user to select a file containing a Sudoku puzzle and validates its content.

    addSudokuFromImage():
        Opens a file dialog for the user to select an image file containing a Sudoku puzzle and processes the image to extract the puzzle.

    generateSudoku():
        Generates a Sudoku puzzle from an API endpoint and opens the Sudoku creator app with the puzzle data.
    """

    def __init__(self, sudoku_picker_app):
        """
        Initializes the SudokuAdderApp instance. This method sets up the 
        initial state of the application and connects the add and go back buttons
        to their respective handlers.

        Parameters
        ----------
        sudoku_picker_app : QApplication
            The main application instance that handles the Sudoku picker.
        """
        super().__init__()
        self.sudoku_picker_app = sudoku_picker_app
        self._connect_add_button()
        self._connect_go_back_button()

    def _connect_add_button(self):
        """Connects the add button click event to the _handle_add_button method."""
        self.add_button.clicked.connect(self._handle_add_button)

    def _connect_go_back_button(self):
        """Connects the go back button click event to the _handle_go_back_button method."""
        self.go_back_button.clicked.connect(self._handle_go_back_button)
    
    def _handle_go_back_button(self):
        """Handles the event when the go back button is clicked, showing the Sudoku picker app and closing the current window."""
        self.sudoku_picker_app.show()
        self.close()

    def _handle_add_button(self):
        """
        Handles the event when the add button is clicked. This method determines
        the source of the Sudoku puzzle based on the user's selection from the combo box.
        """
        options = self.option_combo_box.currentText()
        
        if options == 'Dodaj z pliku':
            self.addSudokuFromFile()
        elif options == 'Stwórz własny':
            self.addSudokuFromUser()
        elif options == 'Dodaj ze zdjecia':
            self.addSudokuFromImage()
        elif options == 'Wygeneruj':
            self.generateSudoku()

    def addSudokuFromUser(self):
        """Opens the Sudoku creator application for the user to manually create a Sudoku puzzle."""
        sudokuCreatorApp = SudokuCreatorApp(sudoku_picker_app=self.sudoku_picker_app)
        sudokuCreatorApp.show()
        self.close()

    def addSudokuFromFile(self):
        """
        Opens a file dialog for the user to select a file containing a Sudoku puzzle.
        Reads the file, validates its content, and if valid, opens the Sudoku creator 
        app with the puzzle data.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, 'Wybierz plik z Sudoku', os.path.expanduser('~'), 'Text Files (*.txt);;All Files (*)')
        if file_path:
            try:
                with open(file_path, 'r'):
                    sudoku_string = get_sudoku_string_from_file(file_path)   
                    valid = is_valid(sudoku_string)

                if valid:
                    sudoku_creator_app = SudokuCreatorApp(sudoku_picker_app=self.sudoku_picker_app, data=sudoku_string)
                    sudoku_creator_app.show()
                    self.close()
                else:
                    QMessageBox.warning(self, 'Błąd', 'Niepoprawny format Sudoku lub Sudoku nie jest rozwiązywalne.')
            except Exception as e:
                QMessageBox.critical(self, 'Błąd', f'Wystąpił błąd podczas wczytywania pliku: {str(e)}')

    def addSudokuFromImage(self):
        """
        Opens a file dialog for the user to select an image file containing a Sudoku puzzle.
        Processes the image to extract the puzzle, validates its content, and if valid, 
        opens the Sudoku creator app with the puzzle data.
        """
        file_path, _ = QFileDialog.getOpenFileName(self, 'Wybierz plik ze zdjęciem Sudoku', os.path.expanduser('~'), 'Photos (*.png *.jpg *.dat);;All Files (*)')

        if file_path:
            try:
                with open(file_path, 'r'):
                    sudoku_list = get_sudoku_from_image(file_path)
                    sudoku_string = ",".join([str(num) for num in sudoku_list])
                    
                    valid = is_valid(sudoku_string)

                if valid:
                    sudoku_creator_app = SudokuCreatorApp(sudoku_picker_app=self.sudoku_picker_app, data=sudoku_string)
                    sudoku_creator_app.show()
                    self.close()
                else:
                    QMessageBox.warning(self, 'Błąd', 'Niepoprawny format Sudoku lub Sudoku nie jest rozwiązywalne.')
            except Exception as e:
                QMessageBox.critical(self, 'Błąd', f'Wystąpił błąd podczas wczytywania pliku: {str(e)}')


    def generateSudoku(self):
        """Generates a Sudoku puzzle from an API endpoint and opens the Sudoku creator app with the puzzle data."""
        try:
            sudoku_string = get_sudoku_from_api()
            sudoku_creator_app = SudokuCreatorApp(sudoku_picker_app=self.sudoku_picker_app, data=sudoku_string)
            sudoku_creator_app.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, 'Błąd', f'Wystąpił błąd podczas generowania Sudoku: {str(e)}')

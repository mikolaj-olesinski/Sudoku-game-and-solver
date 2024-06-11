from model.utils.func import get_sudoku_string_from_file, is_solvable
from view.sudoku_game_gui import SudokuGUI
from controller.controls.sudoku_control import validate_cell_changed_text, hint_for_sudoku, save_sudoku, check_sudoku_for_win
from model.utils.classes import BlankCell
from database.getData import get_timer
from database.addData import addSudoku
from view.sudoku_adder_gui import AddSudokuGUI
from controller.apps.sudoku_creator_app import SudokuCreatorApp
from PySide6.QtWidgets import QMessageBox, QFileDialog
import os

class SudokuAdderApp(AddSudokuGUI):
    def __init__(self, sudoku_picker_app):
        super().__init__()
        self.sudoku_picker_app = sudoku_picker_app
        self._connect_add_button()
        self._connect_go_back_button()

    def _connect_add_button(self):
        self.add_button.clicked.connect(self._handle_add_button)

    def _connect_go_back_button(self):
        self.go_back_button.clicked.connect(self._handle_go_back_button)
    
    def _handle_go_back_button(self):
        self.sudoku_picker_app.show()
        self.close()

    def _handle_add_button(self):
        options = self.option_combo_box.currentText()
        
        if options == 'Dodaj z pliku':
            self.addSudokuFromFile()
        elif options == 'Stwórz własny':
            self.addSudokuFromUser()
        elif options == 'Dodaj ze zdjęcia':
            self.addSudokuFromImage()

    def addSudokuFromUser(self):
        sudokuCreatorApp = SudokuCreatorApp(self.sudoku_picker_app)
        sudokuCreatorApp.show()
        self.close()


    def addSudokuFromFile(self):
 
        file_path, _ = QFileDialog.getOpenFileName(self, 'Wybierz plik z Sudoku', os.path.expanduser('~'), 'Text Files (*.txt);;All Files (*)')
        if file_path:
            try:
                with open(file_path, 'r'):
                    sudoku_string = get_sudoku_string_from_file(file_path)
                    
                is_valid = is_solvable(sudoku_string)
                print(f"Is valid: {is_valid}")
                
                if is_valid:
                    addSudoku(sudoku_string)
                    QMessageBox.information(self, 'Sukces', 'Sudoku zostało wczytane poprawnie!')
                else:
                    QMessageBox.warning(self, 'Błąd', 'Niepoprawny format Sudoku lub Sudoku nie jest rozwiązywalne.')
            except Exception as e:
                QMessageBox.critical(self, 'Błąd', f'Wystąpił błąd podczas wczytywania pliku: {str(e)}')
        


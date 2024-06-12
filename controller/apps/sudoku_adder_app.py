from model.utils.func import get_sudoku_string_from_file, is_valid
from view.sudoku_adder_gui import AddSudokuGUI
from controller.apps.sudoku_creator_app import SudokuCreatorApp
from PySide6.QtWidgets import QMessageBox, QFileDialog
from model.PhotoDetection.sudokiMain import get_sudoku_from_image
import os
import numpy as np

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
        elif options == 'Dodaj ze zdjecia':
            self.addSudokuFromImage()

    def addSudokuFromUser(self):
        sudokuCreatorApp = SudokuCreatorApp(sudoku_picker_app=self.sudoku_picker_app)
        sudokuCreatorApp.show()
        self.close()


    def addSudokuFromFile(self):
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
        print("addSudokuFromImage")
        file_path, _ = QFileDialog.getOpenFileName(self, 'Wybierz plik ze zdjęciem Sudoku', os.path.expanduser('~'), 'Photos (*.png *.jpg *.dat);;All Files (*)')

        if file_path:
            try:
                with open(file_path, 'r'):

                    sudoku = get_sudoku_from_image(file_path)
                    array_str = np.array_str(sudoku, max_line_width=np.inf, precision=0)
                    array_str = array_str.replace('[', '').replace(']', '').replace('\n', '').replace(' ', ',')
                    sudoku_string = array_str
                    valid = is_valid(sudoku_string)

                
                if valid:
                    sudoku_creator_app = SudokuCreatorApp(sudoku_picker_app=self.sudoku_picker_app, data=sudoku_string)
                    sudoku_creator_app.show()
                    self.close()
                else:
                    QMessageBox.warning(self, 'Błąd', 'Niepoprawny format Sudoku lub Sudoku nie jest rozwiązywalne.')
            except Exception as e:
                QMessageBox.critical(self, 'Błąd', f'Wystąpił błąd podczas wczytywania pliku: {str(e)}')


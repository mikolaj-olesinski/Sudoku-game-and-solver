import sys
from PySide6.QtWidgets import QApplication
from controller.apps.login_app import login_app
from view.pick_sudoku_gui import SudokuPicker
from database.create_database import create_database_and_add_basic_sudokus

if __name__ == "__main__":
    create_database_and_add_basic_sudokus("sudoku_database")

    app = QApplication([])
    app.setStyle("Fusion")
    app.setStyleSheet(open('view/style.qss').read())
    ex = login_app()
    sys.exit(app.exec())
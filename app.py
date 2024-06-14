import sys, os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from controller.apps.login_app import login_app
from database.create_database import create_database_and_add_basic_sudokus


if __name__ == "__main__":
    create_database_and_add_basic_sudokus("sudoku_database")

    app = QApplication([])
    app.setStyle("Fusion")
    app.setStyleSheet(open('view/style.qss').read())
    app.setWindowIcon(QIcon(os.path.abspath(os.path.join('constants', 'resources', 'sudoku.png'))))
    ex = login_app()
    sys.exit(app.exec()) 
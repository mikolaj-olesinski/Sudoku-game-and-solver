import sys
from PySide6.QtWidgets import QApplication
from controller.apps.login_app import login_app
from controller.apps.sudoku_app import sudoku_app

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    app.setStyleSheet(open('view/style.qss').read())
    ex = login_app()
    sys.exit(app.exec())

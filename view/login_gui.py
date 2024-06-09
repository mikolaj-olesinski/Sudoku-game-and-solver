import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from controller.apps.sudoku_game_app import sudoku_app

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Logowanie")
        self.setGeometry(100, 100, 300, 150)

        self.username_label = QLabel("Nazwa użytkownika:")
        self.username_input = QLineEdit()
        self.username_input.setObjectName("username_input")
        self.login_button = QPushButton("Zaloguj")
        self.login_button.setObjectName("login_button")

        layout = QVBoxLayout()
        layout.addWidget(self.username_label, alignment=Qt.AlignCenter)  
        layout.addWidget(self.username_input)
        layout.addWidget(self.login_button, alignment=Qt.AlignCenter)


        layout.setContentsMargins(20, 20, 20, 20)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def open_sudoku(self, app):
        self.hide()
        sudoku_app(app)



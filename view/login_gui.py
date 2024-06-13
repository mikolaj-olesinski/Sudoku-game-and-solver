from PySide6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from controller.apps.sudoku_game_app import sudoku_app

class LoginWindow(QMainWindow):
    """
    QMainWindow subclass representing the login window for the Sudoku game application.

    Attributes:
    - username_label (QLabel): Label widget for displaying "Nazwa użytkownika:".
    - username_input (QLineEdit): Line edit widget for entering the username.
    - login_button (QPushButton): Button widget for initiating the login process.

    Methods:
    - __init__(): Initializes the LoginWindow with username label, input field, and login button.
    - open_sudoku(app): Hides the current login window and opens the Sudoku game application with the given 'app' parameter.
    """

    def __init__(self):
        """
        Initializes the LoginWindow with necessary widgets and layout.
        """
        super().__init__()

        self.setWindowTitle("Logowanie")
        self.setGeometry(100, 100, 300, 150)

        # Widgets setup
        self.username_label = QLabel("Nazwa użytkownika:")
        self.username_input = QLineEdit()
        self.username_input.setObjectName("username_input")
        self.login_button = QPushButton("Zaloguj")
        self.login_button.setObjectName("login_button")

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.username_label, alignment=Qt.AlignCenter)  
        layout.addWidget(self.username_input)
        layout.addWidget(self.login_button, alignment=Qt.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)

        # Main widget setup
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

    def open_sudoku(self, app):
        """
        Opens the Sudoku game application window.

        Args:
        - app: An instance of the Sudoku game application.

        This method hides the current login window and shows the Sudoku game application window.
        """
        self.hide()
        sudoku_app(app)

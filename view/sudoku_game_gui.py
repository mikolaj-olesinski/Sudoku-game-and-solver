from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtGui import QPixmap
from model.utils.classes import Stoper
from model.sudoku_class import Sudoku as SudokuWidget
from PySide6.QtCore import Qt
import os

class TopWidget(QWidget):
    """
    QWidget subclass representing the top widget for the Sudoku game GUI.

    Attributes:
    - stoper (Stoper): Instance of Stoper class for timing.
    - cofniecie (QPushButton): Button for navigating back.

    Methods:
    - __init__(): Initializes the TopWidget with a back button and timer.
    - initUI(): Sets up the UI layout and adds the back button and timer widget.
    """

    def __init__(self):
        """
        Initializes the TopWidget with necessary widgets and layout.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Sets up the UI layout for TopWidget and adds the back button and timer widget.
        """
        layout = QHBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Load back icon from resources
        back_icon_path = os.path.abspath(os.path.join("constants", "resources", "back.png"))
        cofniecie_icon = QPixmap(back_icon_path).scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        cofniecie = QPushButton()
        cofniecie.setIcon(cofniecie_icon)
        cofniecie.setIconSize(cofniecie_icon.size())
        cofniecie.setFixedSize(cofniecie_icon.size())

        # Initialize stopwatch widget
        stoper = Stoper()
        
        layout.addWidget(cofniecie)
        layout.addWidget(stoper, alignment=Qt.AlignRight)

        self.stoper = stoper
        self.cofniecie = cofniecie


class BottomWidget(QWidget):
    """
    QWidget subclass representing the bottom widget for the Sudoku game GUI.

    Attributes:
    - save_button (QPushButton): Button for saving the current Sudoku game.
    - hint_button (QPushButton): Button for getting a hint in the Sudoku game.

    Methods:
    - __init__(): Initializes the BottomWidget with save and hint buttons.
    - initUI(): Sets up the UI layout and adds the save and hint buttons.
    """

    def __init__(self):
        """
        Initializes the BottomWidget with necessary widgets and layout.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Sets up the UI layout for BottomWidget and adds the save and hint buttons.
        """
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        save_button = QPushButton("Zapisz")
        save_button.setObjectName("save_button")

        hint_button = QPushButton("Podpowiedz")
        hint_button.setObjectName("hint_button")

        layout.addWidget(save_button)
        layout.addWidget(hint_button)

        self.hint_button = hint_button
        self.save_button = save_button


class SudokuGUI(QWidget):
    """
    QWidget subclass representing the main Sudoku game GUI.

    Attributes:
    - top_widget (TopWidget): Top widget containing navigation and timer.
    - sudoku (SudokuWidget): Widget for playing Sudoku.
    - bottom_widget (BottomWidget): Bottom widget containing save and hint buttons.

    Methods:
    - __init__(): Initializes the SudokuGUI with top, sudoku, and bottom widgets.
    - initUI(): Sets up the main layout and adds the top, sudoku, and bottom widgets.
    """

    def __init__(self):
        """
        Initializes the SudokuGUI with necessary widgets and layout.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Sets up the main UI layout for SudokuGUI and adds top, sudoku, and bottom widgets.
        """
        main_layout = QVBoxLayout()

        self.top_widget = TopWidget()
        self.sudoku = SudokuWidget()
        self.bottom_widget = BottomWidget()

        main_layout.addWidget(self.top_widget)
        main_layout.addWidget(self.sudoku)
        main_layout.addWidget(self.bottom_widget)

        self.setLayout(main_layout)
        self.setWindowTitle('Sudoku Application')
        self.setGeometry(100, 100, 700, 600)

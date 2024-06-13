from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtGui import QPixmap
from model.sudoku_class import Sudoku as SudokuWidget
from PySide6.QtCore import Qt
import os

class TopWidgetForCreator(QWidget):
    """
    QWidget subclass representing the top widget for the Sudoku creator GUI.

    Attributes:
    - cofniecie (QPushButton): Button for navigating back.
    
    Methods:
    - __init__(): Initializes the TopWidgetForCreator with a back button.
    - initUI(): Sets up the layout and adds the back button to the widget.
    """

    def __init__(self):
        """
        Initializes the TopWidgetForCreator with necessary widgets and layout.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Sets up the UI layout for TopWidgetForCreator and adds the back button.
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

        layout.addWidget(cofniecie, alignment=Qt.AlignLeft)

        self.cofniecie = cofniecie


class BottomWidgetForCreator(QWidget):
    """
    QWidget subclass representing the bottom widget for the Sudoku creator GUI.

    Attributes:
    - save_button (QPushButton): Button for saving the Sudoku puzzle.

    Methods:
    - __init__(): Initializes the BottomWidgetForCreator with a save button.
    - initUI(): Sets up the UI layout and adds the save button to the widget.
    """

    def __init__(self):
        """
        Initializes the BottomWidgetForCreator with necessary widgets and layout.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Sets up the UI layout for BottomWidgetForCreator and adds the save button.
        """
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        save_button = QPushButton("Zapisz")
        save_button.setObjectName("save_button")

        layout.addWidget(save_button)

        self.save_button = save_button


class SudokuCreatorGUI(QWidget):
    """
    QWidget subclass representing the main Sudoku creator GUI.

    Attributes:
    - top_widget (TopWidgetForCreator): Top widget containing navigation and back button.
    - sudoku (SudokuWidget): Widget for creating and editing Sudoku puzzles.
    - bottom_widget (BottomWidgetForCreator): Bottom widget containing save button.

    Methods:
    - __init__(): Initializes the SudokuCreatorGUI with top, sudoku, and bottom widgets.
    - initUI(): Sets up the main layout and adds the top, sudoku, and bottom widgets.
    """

    def __init__(self):
        """
        Initializes the SudokuCreatorGUI with necessary widgets and layout.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Sets up the main UI layout for SudokuCreatorGUI and adds top, sudoku, and bottom widgets.
        """
        main_layout = QVBoxLayout()

        self.top_widget = TopWidgetForCreator()
        self.sudoku = SudokuWidget()
        self.bottom_widget = BottomWidgetForCreator()

        main_layout.addWidget(self.top_widget)
        main_layout.addWidget(self.sudoku)
        main_layout.addWidget(self.bottom_widget)

        self.setLayout(main_layout)
        self.setWindowTitle('Sudoku Application')
        self.setGeometry(100, 100, 700, 600)

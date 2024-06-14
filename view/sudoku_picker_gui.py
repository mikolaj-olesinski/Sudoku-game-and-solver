from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os
from model.sudoku_picker import SudokuPicker

class TopWidgetForSudokuPicker(QWidget):
    """
    QWidget subclass representing the top widget for the SudokuPicker GUI.

    Attributes:
    - cofniecie (QPushButton): Button for navigating back.

    Methods:
    - __init__(): Initializes the TopWidgetForSudokuPicker with a back button.
    - initUI(): Sets up the UI layout and adds the back button.
    """

    def __init__(self):
        """
        Initializes the TopWidgetForSudokuPicker with necessary widgets and layout.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Sets up the UI layout for TopWidgetForSudokuPicker and adds the back button.
        """
        layout = QHBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(20, 20, 0, 0)
        self.setLayout(layout)
        self.setFixedHeight(50)

        back_icon_path = os.path.abspath(os.path.join("constants", "resources", "back.png"))
        cofniecie_icon = QPixmap(back_icon_path).scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        cofniecie = QPushButton()
        cofniecie.setIcon(cofniecie_icon)
        cofniecie.setIconSize(cofniecie_icon.size())
        cofniecie.setFixedSize(cofniecie_icon.size())

        layout.addWidget(cofniecie, alignment=Qt.AlignLeft | Qt.AlignBottom)
        self.cofniecie = cofniecie


class BottomWidgetForSudokuPicker(QWidget):
    """
    QWidget subclass representing the bottom widget for the SudokuPicker GUI.

    Attributes:
    - add_sudoku_button (QPushButton): Button for adding a new Sudoku puzzle.

    Methods:
    - __init__(): Initializes the BottomWidgetForSudokuPicker with an add Sudoku button.
    - initUI(): Sets up the UI layout and adds the add Sudoku button.
    """

    def __init__(self):
        """
        Initializes the BottomWidgetForSudokuPicker with necessary widgets and layout.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Sets up the UI layout for BottomWidgetForSudokuPicker and adds the add Sudoku button.
        """
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(30, 0, 30, 30)

        add_sudoku_button = QPushButton("Dodaj sudoku")
        layout.addWidget(add_sudoku_button)
        self.add_sudoku_button = add_sudoku_button


class SudokuPickerGUI(QWidget):
    """
    QWidget subclass representing the main SudokuPicker GUI.

    Attributes:
    - user_id (str): Identifier of the current user.
    - top_widget (TopWidgetForSudokuPicker): Top widget containing navigation.
    - sudoku_picker (SudokuPicker): Widget for displaying Sudoku puzzles.
    - bottom_widget (BottomWidgetForSudokuPicker): Bottom widget containing add Sudoku button.

    Methods:
    - __init__(user_id): Initializes the SudokuPickerGUI with top, SudokuPicker, and bottom widgets.
    - initUI(): Sets up the main UI layout and adds top, SudokuPicker, and bottom widgets.
    - _setWindowSize(): Adjusts the window size based on the SudokuPicker table view width.
    """

    def __init__(self, user_id):
        """
        Initializes the SudokuPickerGUI with necessary widgets and layout.

        Args:
        - user_id (str): Identifier of the current user.
        """
        super().__init__()
        self.user_id = user_id
        self.initUI()
        self._setWindowSize()

    def initUI(self):
        """
        Sets up the main UI layout for SudokuPickerGUI and adds top, SudokuPicker, and bottom widgets.
        """
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.top_widget = TopWidgetForSudokuPicker()
        self.sudoku_picker = SudokuPicker(self.user_id)
        self.bottom_widget = BottomWidgetForSudokuPicker()

        main_layout.addWidget(self.top_widget)
        main_layout.addWidget(self.sudoku_picker)
        main_layout.addWidget(self.bottom_widget)

        self.setLayout(main_layout)
        self.setWindowTitle('Sudoku Application')

    def _setWindowSize(self):
        """
        Adjusts the window size based on the width of the SudokuPicker table view.
        """
        table_width = self.sudoku_picker.table_view.horizontalHeader().length() + 30
        self.setContentsMargins(0, 0, 0, 0)
        self.resize(table_width, 400)

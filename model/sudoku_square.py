from PySide6.QtWidgets import QWidget, QGridLayout, QLineEdit
from PySide6.QtCore import Qt
from model.utils.classes import NonZeroValidator

class SudokuSquare(QWidget):
    """
    Widget representing a 3x3 Sudoku square.

    Attributes:
    - cells (list): 2D list containing QLineEdit objects representing individual cells in the Sudoku square.

    Methods:
    - __init__(): Initializes the SudokuSquare widget and calls initUI() to set up the user interface.
    - initUI(): Sets up the grid layout and initializes the QLineEdit cells with alignment, size, validator, and length constraints.
    - validate_square(cell): Validates the Sudoku square by checking if adding a value to a cell maintains Sudoku rules within the square.
    - check_square_for_win(): Checks if all cells in the Sudoku square are filled with unique numbers from 1 to 9.
    """

    def __init__(self):
        """
        Initializes the SudokuSquare widget.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Sets up the user interface for the SudokuSquare widget:
        - Creates a QGridLayout for arranging QLineEdit cells.
        - Initializes QLineEdit cells with alignment, size, validator, and length constraints.
        """
        layout = QGridLayout()
        self.setLayout(layout)
        layout.setSpacing(0)

        self.cells = []

        for row in range(3):
            row_cells = []
            for col in range(3):
                cell = QLineEdit()
                cell.setAlignment(Qt.AlignCenter)
                cell.setFixedSize(80, 80)
                cell.setValidator(NonZeroValidator())
                cell.setMaxLength(1)
                layout.addWidget(cell, row, col)
                layout.setContentsMargins(0, 0, 0, 0)
                row_cells.append(cell)
            self.cells.append(row_cells)

    def validate_square(self, cell):
        """
        Validates the Sudoku square after a cell value has been changed.

        Args:
        - cell (QLineEdit): The cell whose value has been changed.

        Returns:
        - bool: True if the Sudoku square is valid after the change, False otherwise.
        """
        if cell.text() == '':
            return True
        
        numbers = []
        for i in range(3):
            for j in range(3):
                cell = self.cells[i][j]
                if cell.text():
                    numbers.append(cell.text())
        
        if len(numbers) != len(set(numbers)):
            return False
        return True
    
    def check_square_for_win(self):
        """
        Checks if the Sudoku square contains all unique numbers from 1 to 9.

        Returns:
        - bool: True if the Sudoku square contains all unique numbers from 1 to 9, False otherwise.
        """
        numbers = []
        for i in range(3):
            for j in range(3):
                cell = self.cells[i][j]
                if cell.text():
                    numbers.append(cell.text())
        
        if len(set(numbers)) == 9:
            return True
        return False

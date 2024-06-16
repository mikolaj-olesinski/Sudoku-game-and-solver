from PySide6.QtWidgets import QWidget, QGridLayout
from model.utils.classes import BlankCell, ComputerCell, SolvedCell
from model.sudoku_square import SudokuSquare

class Sudoku(QWidget):
    """
    Represents a Sudoku game board widget.

    Attributes:
    - cells (dict): Dictionary mapping cell names to cell objects.
    - squares (dict): Dictionary mapping square names to square objects.
    - id (int or None): ID of the Sudoku game.
    - user_id (int or None): ID of the user playing the Sudoku game.

    Methods:
    - initUI(): Initializes the Sudoku board UI layout.
    - initializeCellsAndSquares(): Initializes cells and squares dictionaries.
    - validate_row(cell): Validates a row in the Sudoku board.
    - validate_column(cell): Validates a column in the Sudoku board.
    - update_board(board, sudoku_id=None, blank_cell_color='blue'): Updates the Sudoku board with new data.
    - update_colors_on_board(): Updates the colors of cells on the Sudoku board based on validation rules.
    - switch_cell(new_cell, x_row, y_column): Switches a cell in the Sudoku board with a new cell.
    """

    def __init__(self):
        """
        Initializes the Sudoku widget.

        Initializes the UI, cells, squares, ID, and user ID attributes.
        """
        super().__init__()

        self.initUI()
        self.cells, self.squares = self.initializeCellsAndSquares()
        self.id = None
        self.user_id = None

    def initUI(self):
        """
        Initializes the UI layout for the Sudoku widget.

        Sets up a grid layout and initializes Sudoku squares.
        """
        self.setGeometry(100, 100, 700, 700)

        grid = QGridLayout()
        grid.setSpacing(0)
        self.setLayout(grid)

        self.squares = []

        for row in range(3):
            row_squares = []
            for col in range(3):
                square = SudokuSquare()
                grid.addWidget(square, row, col)
                row_squares.append(square)
            self.squares.append(row_squares)

    def initializeCellsAndSquares(self):
        """
        Initializes cells and squares dictionaries.

        Returns:
        - tuple: (cells, squares) where cells is a dictionary mapping cell names to cell objects,
                 and squares is a dictionary mapping square names to square objects.
        """
        cells = {}
        squares = {}

        for i, row in enumerate(self.squares):
            for j, square in enumerate(row):
                square.setObjectName(f'square_{i}_{j}')
                squares[f'square_{i}_{j}'] = square

                for x, row in enumerate(square.cells):
                    for y, cell in enumerate(row):
                        cell_name = f'cell_{i * 3 + x}_{j * 3 + y}'
                        cell.setObjectName(cell_name)
                        cells[cell_name] = cell

        return cells, squares

    def validate_row(self, cell):
        """
        Validates a row in the Sudoku board.

        Args:
        - cell (QWidget): Cell widget to validate.

        Returns:
        - bool: True if the row is valid, False otherwise.
        """
        if cell.text() == '':
            return True
        
        row = int(cell.objectName().split('_')[1])
        numbers = []
        for i in range(9):
            cell = self.cells[f'cell_{row}_{i}']
            if cell.text():
                numbers.append(cell.text())
            
        if len(numbers) != len(set(numbers)):
            return False
        return True

    def validate_column(self, cell):
        """
        Validates a column in the Sudoku board.

        Args:
        - cell (QWidget): Cell widget to validate.

        Returns:
        - bool: True if the column is valid, False otherwise.
        """
        if cell.text() == '':
            return True
        
        column = int(cell.objectName().split('_')[2])
        numbers = []
        for i in range(9):
            cell = self.cells[f'cell_{i}_{column}']
            if cell.text():
                numbers.append(cell.text())
        
        if len(numbers) != len(set(numbers)):
            return False
        return True
    
    def update_board(self, board, sudoku_id=None, blank_cell_color='blue'):
        """
        Updates the Sudoku board with new data.

        Args:
        - board (dict): Dictionary mapping cell names to cell values.
        - sudoku_id (int or None): ID of the Sudoku game.
        - blank_cell_color (str): Color of blank cells.

        Updates the board based on the given data and updates cell colors.
        """
        self.id = sudoku_id

        for cell_name, value in board.items():
            
            if value != '0':
                if value[0] == 'C':
                    cell = ComputerCell()
                    self.switch_cell(cell, int(cell_name.split('_')[1]), int(cell_name.split('_')[2]))
                    cell.setText(value[1])
                elif value in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    cell = BlankCell(blank_cell_color)
                    self.switch_cell(cell, int(cell_name.split('_')[1]), int(cell_name.split('_')[2]))
                    cell.setText(value)

                elif value[0] == 'S':
                    cell = SolvedCell()
                    self.switch_cell(cell, int(cell_name.split('_')[1]), int(cell_name.split('_')[2]))
                    cell.setText(value[1])

            
            else:
                cell = BlankCell(blank_cell_color)
                self.switch_cell(cell, int(cell_name.split('_')[1]), int(cell_name.split('_')[2]))
                cell.setText('')
                
            if isinstance(cell, BlankCell) and cell.text() != '':
                cell_row = int(cell.objectName().split('_')[1])
                cell_col = int(cell.objectName().split('_')[2])
                square_row = cell_row // 3
                square_col = cell_col // 3

                square = self.squares[f'square_{square_row}_{square_col}']
                if not square.validate_square(cell) or not self.validate_column(cell) or not self.validate_row(cell):
                    cell.setStyleSheet("color: red;")



    def update_colors_on_board(self):
        """
        Updates the colors of cells on the Sudoku board based on validation rules.
        """
        for _, cell in self.cells.items():
            if isinstance(cell, BlankCell) and cell.text() != '':
                cell_row = int(cell.objectName().split('_')[1])
                cell_col = int(cell.objectName().split('_')[2])

                square_row = cell_row // 3
                square_col = cell_col // 3

                square = self.squares[f'square_{square_row}_{square_col}']
                if not square.validate_square(cell) or not self.validate_column(cell) or not self.validate_row(cell):
                    cell.setStyleSheet("color: red;")

    def switch_cell(self, new_cell, x_row, y_column):
        """
        Switches a cell in the Sudoku board with a new cell.

        Args:
        - new_cell (QWidget): New cell widget to switch with.
        - x_row (int): Row index of the cell.
        - y_column (int): Column index of the cell.

        Replaces the old cell with the new cell in the board and updates the layout.
        """
        old_cell = self.cells[f'cell_{x_row}_{y_column}']
        self.cells[f'cell_{x_row}_{y_column}'] = new_cell

        new_cell.copy_properties(old_cell)

        square, layout = old_cell.parent(), old_cell.parent().layout()
        square.cells[x_row % 3][y_column % 3] = new_cell
        layout.replaceWidget(old_cell, new_cell)

        old_cell.deleteLater()

import sys
from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QLineEdit, QFrame
from PySide6.QtCore import Qt
from nwm import NonZeroValidator, UserCell, ComputerCell, BlankCell
from sudoku_square import SudokuSquare

class Sudoku(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.cells, self.squares = self.initializeCellsAndSquares()


    def initUI(self):
        self.setGeometry(100, 100, 700, 700)

        grid = QGridLayout()
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

    def validate_row(self, row):
        numbers = []
        for i in range(9):
            cell = self.cells[f'cell_{row}_{i}']
            if cell.text():
                numbers.append(cell.text())
            
        if len(numbers) != len(set(numbers)):
            return False
        return True

    def validate_column(self, column):
        numbers = []
        for i in range(9):
            cell = self.cells[f'cell_{i}_{column}']
            if cell.text():
                numbers.append(cell.text())
        
        if len(numbers) != len(set(numbers)):
            return False
        return True
    

    def update_board(self, board):
        for cell_name, value in board.items():
            old_cell = self.cells[cell_name]
            
            if value != '0':
                if value[0] == 'C':
                    cell = ComputerCell()
                    self.switch_cell(cell, int(cell_name.split('_')[1]), int(cell_name.split('_')[2]))
                    cell.setText(value[1])
                elif value[0] == 'U':
                    cell = UserCell()
                    self.switch_cell(cell, int(cell_name.split('_')[1]), int(cell_name.split('_')[2]))
                    cell.setText(value[1])

            
            else:
                cell = BlankCell()
                self.switch_cell(cell, int(cell_name.split('_')[1]), int(cell_name.split('_')[2]))
                cell.setText('')



    def switch_cell(self, new_cell, x_row, y_column):
        old_cell = self.cells[f'cell_{x_row}_{y_column}']
        self.cells[f'cell_{x_row}_{y_column}'] = new_cell

        new_cell.copy_properties(old_cell)

        square, layout = old_cell.parent(), old_cell.parent().layout()
        square.cells[x_row % 3][y_column % 3] = new_cell
        layout.replaceWidget(old_cell, new_cell)

        old_cell.deleteLater()
 

            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = SudokuGUI()
    main_window.show()
    sys.exit(app.exec())

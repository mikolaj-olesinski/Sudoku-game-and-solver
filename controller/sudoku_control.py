from model.utils.classes import ComputerCell

def validate_cell_changed_text(cell, sudoku):
    cell_row = int(cell.objectName().split('_')[1])
    cell_col = int(cell.objectName().split('_')[2])

    square_row = cell_row // 3
    square_col = cell_col // 3

    square = sudoku.squares[f'square_{square_row}_{square_col}']
    if not square.validate_square(cell_row, cell_col) or not sudoku.validate_column(cell_col) or not sudoku.validate_row(cell_row):
        cell.setStyleSheet('color: #b56')
        return False
    else:
        if not isinstance(cell, ComputerCell):
            cell.setStyleSheet('color: #458;')
        return True

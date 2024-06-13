from model.utils.classes import ComputerCell, SolvedCell
from model.utils.func import get_hint_for_sudoku, databaseData_to_grid, get_data_from_sudoku, get_saved_data_from_sudoku, check_win
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Sudoku_model, UsersSudoku_model
from database.resetData import resetUsersSudoku
from datetime import datetime
from PySide6.QtWidgets import QMessageBox

def validate_cell_changed_text(cell, sudoku, color='blue'):
    """
    Validates the text entered in a Sudoku cell based on Sudoku rules.

    Parameters
    ----------
    cell : QWidget
        The cell widget in the Sudoku grid.
    sudoku : SudokuGUI
        The Sudoku game instance that contains the Sudoku grid.
    color : str, optional
        The color of the text in the cell upon validation (default is 'blue').

    Returns
    -------
    bool
        True if the cell text is valid according to Sudoku rules, False otherwise.
    """
    cell_row = int(cell.objectName().split('_')[1])
    cell_col = int(cell.objectName().split('_')[2])

    square_row = cell_row // 3
    square_col = cell_col // 3

    square = sudoku.squares[f'square_{square_row}_{square_col}']
    if not square.validate_square(cell) or not sudoku.validate_column(cell) or not sudoku.validate_row(cell):
        cell.setStyleSheet('color: red;')
        return False
    else:
        if not isinstance(cell, ComputerCell):
            cell.setStyleSheet(f'color: {color};')
        return True

def hint_for_sudoku(sudoku, row=None, col=None):
    """
    Provides a hint for the Sudoku puzzle.

    This function retrieves the solved Sudoku data from the database, compares it with the current Sudoku data,
    and suggests the next correct value for the specified cell or any empty cell if not specified.

    Parameters
    ----------
    sudoku : SudokuGUI
        The Sudoku game instance that contains the Sudoku grid.
    row : int, optional
        The row index of the cell to provide a hint for (default is None).
    col : int, optional
        The column index of the cell to provide a hint for (default is None).
    """
    db_name = 'sudoku_database'
    engine = create_engine(f'sqlite:///database/{db_name}.sqlite3')

    Session = sessionmaker(bind=engine)
    session = Session()

    sudoku_model = session.query(Sudoku_model).filter(Sudoku_model.id == sudoku.id).first()

    solved_data = databaseData_to_grid(sudoku_model.solved_data)
    data = get_data_from_sudoku(sudoku)
    data = databaseData_to_grid(data)

    if row is None or col is None:
        row, col, value = get_hint_for_sudoku(data, solved_data)
    else:
        value = solved_data[row][col]

    cell = SolvedCell()
    sudoku.switch_cell(cell, row, col)
    cell.setText(str(value))
    cell.setFocus()

def save_sudoku(sudoku):
    """
    Saves the current state of the Sudoku puzzle to the database.

    Parameters
    ----------
    sudoku : SudokuGUI
        The Sudoku game instance that contains the Sudoku grid.
    """
    user_id = sudoku.user_id
    db_name = 'sudoku_database'
    engine = create_engine(f'sqlite:///database/{db_name}.sqlite3')

    Session = sessionmaker(bind=engine)
    session = Session()

    saved_data = get_saved_data_from_sudoku(sudoku)

    users_sudoku_model = session.query(UsersSudoku_model).filter(UsersSudoku_model.sudoku_id == sudoku.id, UsersSudoku_model.user_id == user_id).first()

    if users_sudoku_model.started_at is None:
        users_sudoku_model.started_at = datetime.now()

    users_sudoku_model.current_sudoku_state = saved_data
    users_sudoku_model.last_saved = datetime.now()
    session.commit()

def check_sudoku_for_win(sudoku_app):
    """
    Checks if the Sudoku puzzle is solved.

    If the Sudoku puzzle is solved, displays a congratulatory message, resets the Sudoku puzzle in the database,
    and navigates back to the previous screen.

    Parameters
    ----------
    sudoku_app : sudoku_app
        The Sudoku application instance that contains the Sudoku game.
    
    Returns
    -------
    bool
        True if the Sudoku puzzle is solved, False otherwise.
    """
    if check_win(sudoku_app.sudoku):
        QMessageBox.about(sudoku_app, "Gratulacje", "Gratulacje, udało Ci się rozwiązać sudoku!")
        resetUsersSudoku(sudoku_app.sudoku.user_id, sudoku_app.sudoku.id)
        sudoku_app._handle_back_button()
        return True

    return False

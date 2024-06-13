from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import UsersSudoku_model, Sudoku_model, User_model
from model.utils.classes import BlankCell, ComputerCell, SolvedCell
import random, re

def get_board_from_file(filename):
    """
    Retrieves a Sudoku board from a file.

    Args:
    - filename (str): Name of the file containing Sudoku board data.

    Returns:
    - dict: Dictionary representing the Sudoku board.
    """
    with open(filename, 'r') as file:
        content = file.read().replace('\n', '').split(',')

    board = {}
    for i in range(9):
        for j in range(9):
            board[f'cell_{i}_{j}'] = content[i * 9 + j]

    return board

def get_board_from_db(sudoku_id, user_id):
    """
    Retrieves a Sudoku board from the database based on sudoku_id and user_id.

    Args:
    - sudoku_id (int): ID of the Sudoku puzzle.
    - user_id (int): ID of the user who owns the Sudoku puzzle.

    Returns:
    - dict: Dictionary representing the Sudoku board.
    """
    db_name = 'sudoku_database'
    engine = create_engine(f'sqlite:///database/{db_name}.sqlite3')

    Session = sessionmaker(bind=engine)
    session = Session()

    sudoku = session.query(UsersSudoku_model).filter(UsersSudoku_model.sudoku_id == sudoku_id, UsersSudoku_model.user_id == user_id).first()
    data = sudoku.current_sudoku_state.split(',')

    board = {}
    for i in range(9):
        for j in range(9):
            board[f'cell_{i}_{j}'] = data[i * 9 + j]

    session.close()
    return board

def get_board_from_string(data):
    """
    Retrieves a Sudoku board from a string representation.

    Args:
    - data (str): String representation of the Sudoku board.

    Returns:
    - dict: Dictionary representing the Sudoku board.
    """
    data = data.split(',')
    board = {}
    for i in range(9):
        for j in range(9):
            board[f'cell_{i}_{j}'] = data[i * 9 + j]

    return board

def get_data_from_sudoku(sudoku):
    """
    Retrieves data from a Sudoku puzzle.

    Args:
    - sudoku (object): Sudoku object containing cell data.

    Returns:
    - str: String representation of the Sudoku puzzle data.
    """
    cells = sudoku.cells
    string = ''

    for i in range(9):
        for j in range(9):
            if cells[f"cell_{i}_{j}"].text():
                string += f'{cells[f"cell_{i}_{j}"].text()},'
            else:
                string += '0,'
    return string[:-1]

def get_saved_data_from_sudoku(sudoku):
    """
    Retrieves saved data from a Sudoku puzzle.

    Args:
    - sudoku (object): Sudoku object containing cell data.

    Returns:
    - str: String representation of the saved Sudoku puzzle data.
    """
    cells = sudoku.cells
    string = ''

    for i in range(9):
        for j in range(9):
            cell = cells[f"cell_{i}_{j}"]
            if cell.text():
                if isinstance(cell, ComputerCell):
                    string += f'C{cells[f"cell_{i}_{j}"].text()},'
                elif isinstance(cell, SolvedCell):
                    string += f'S{cells[f"cell_{i}_{j}"].text()},'
                else:
                    string += f'{cells[f"cell_{i}_{j}"].text()},'

            else:
                string += '0,'
    return string[:-1]

def sudoku_data_to_saved_sudoku_data(data):
    """
    Converts Sudoku puzzle data to saved Sudoku puzzle data format.

    Args:
    - data (str): String representation of Sudoku puzzle data.

    Returns:
    - str: String representation of saved Sudoku puzzle data.
    """
    list_data = data.split(',')
    new_data = ''
    for i in list_data:
        if i != '0':
            i = f'C{i}'
        else:
            i = '0'
        new_data += i + ','
    return new_data[:-1]

def isValid(grid, r, c, k):
    """
    Checks if placing a number k at position (r, c) in the Sudoku grid is valid.

    Args:
    - grid (list): 2D list representing the Sudoku grid.
    - r (int): Row index.
    - c (int): Column index.
    - k (int): Number to be placed in the cell.

    Returns:
    - bool: True if valid placement, False otherwise.
    """
    for i in range(9):
        if grid[r][i] == k or grid[i][c] == k:
            return False
    
    startRow, startCol = 3 * (r // 3), 3 * (c // 3)
    for i in range(3):
        for j in range(3):
            if grid[startRow + i][startCol + j] == k:
                return False
    
    return True

def solve_sudoku(grid, r=0, c=0, steps=None):
    """
    Solves the Sudoku grid using backtracking algorithm.

    Args:
    - grid (list): 2D list representing the Sudoku grid.
    - r (int): Row index (default: 0).
    - c (int): Column index (default: 0).
    - steps (dict): Dictionary to track solving steps (default: None).

    Returns:
    - Tuple[bool, dict]: Tuple containing a boolean indicating if Sudoku is solved and steps taken.
    """
    if steps is None:
        steps = {'basic': 0, 'advanced': 0}

    if r == 9:
        return True, steps
    if c == 9:
        return solve_sudoku(grid, r + 1, 0, steps)
    if grid[r][c] != 0:
        return solve_sudoku(grid, r, c + 1, steps)
    else:
        for k in range(1, 10):
            if isValid(grid, r, c, k):
                grid[r][c] = k
                steps['basic'] += 1 
                solved, steps = solve_sudoku(grid, r, c + 1, steps)
                if solved:
                    return True, steps
                grid[r][c] = 0
        steps['advanced'] += 1
        return False, steps

def rate_difficulty(steps):
    """
    Rates the difficulty of solving a Sudoku puzzle based on solving steps.

    Args:
    - steps (dict): Dictionary containing basic and advanced solving steps.

    Returns:
    - str: Difficulty rating ("Easy", "Medium", "Hard", "Very Hard").
    """
    basic_steps = steps['basic']
    advanced_steps = steps['advanced']
    
    if basic_steps > 40 and advanced_steps < 10:
        return "Easy"
    elif basic_steps > 30 and advanced_steps < 20:
        return "Medium"
    elif basic_steps > 20 and advanced_steps < 30:
        return "Hard"
    else:
        return "Very Hard"

def find_difficulty(isSolved, steps):
    """
    Determines the difficulty of a Sudoku puzzle based on its solution status and solving steps.

    Args:
    - isSolved (bool): True if Sudoku is solved, False otherwise.
    - steps (dict): Dictionary containing basic and advanced solving steps.

    Returns:
    - str: Difficulty rating ("Easy", "Medium", "Hard", "Very Hard" or "Unsolvable").
    """
    if isSolved:
        return rate_difficulty(steps)
    else:
        return "Unsolvable"

def get_hint_for_sudoku(data, solved):
    """
    Generates a hint for solving a Sudoku puzzle.

    Args:
    - data (list): 2D list representing the unsolved Sudoku puzzle.
    - solved (list): 2D list representing the solved Sudoku puzzle.

    Returns:
    - Tuple[int, int, int] or None: Tuple containing (row, column, value) of the hint or None if no hint available.
    """
    empty_positions = [(i, j) for i in range(9) for j in range(9) if data[i][j] == 0]

    if not empty_positions:
        return None

    i, j = random.choice(empty_positions)
    return i, j, solved[i][j]

def flatten_to_string(lst):
    """
    Flattens a 2D list into a string separated by commas.

    Args:
    - lst (list): 2D list to be flattened.

    Returns:
    - str: Flattened string representation of the list.
    """
    flattened = [str(item) for sublist in lst for item in sublist]
    return ','.join(flattened)

def databaseData_to_grid(string):
    """
    Converts saved Sudoku puzzle data string into a 2D grid.

    Args:
    - string (str): String representation of saved Sudoku puzzle data.

    Returns:
    - list: 2D list representing the Sudoku grid.
    """
    data = string.split(',')
    grid = []
    for i in range(9):
        row = []
        for j in range(9):
            if data[i * 9 + j][0] in ['S', 'C']:
                row.append(int(data[i * 9 + j][1]))
            else:
                row.append(int(data[i * 9 + j]))
        grid.append(row)
    return grid

def check_username(username):
    """
    Validates a username based on length and character requirements.

    Args:
    - username (str): Username to be validated.

    Returns:
    - bool: True if the username is valid, False otherwise.
    """
    if len(username) > 15 or len(username) < 3:
        print('Username must be between 3 and 15 characters')
        return False

    if not re.match("^[a-zA-Z0-9]*$", username):
        print('Username must contain only letters and numbers')
        return False

    print('Username is valid')
    return True

def get_sudoku_string_from_file(filename):
    """
    Reads Sudoku board data from a file and returns it as a string.

    Args:
    - filename (str): Name of the file containing Sudoku board data.

    Returns:
    - str: Comma-separated string representation of Sudoku board data.
    """
    with open(filename, 'r') as file:
        content = file.read().replace('\n', '').split(',')

    string = ",".join(content)
    return string

def import_data_from_db(user_id):
    """
    Imports Sudoku puzzle data from the database for a specific user.

    Args:
    - user_id (int): ID of the user.

    Returns:
    - list: List of lists containing Sudoku puzzle data and metadata.
    """
    db_name = 'sudoku_database'
    engine = create_engine(f'sqlite:///database/{db_name}.sqlite3')

    Session = sessionmaker(bind=engine)
    session = Session()
    
    users_sudoku = session.query(UsersSudoku_model).filter(UsersSudoku_model.user_id == user_id).all()

    data = []
    for user_sudoku in users_sudoku:
        sudoku = session.query(Sudoku_model).filter(Sudoku_model.id == user_sudoku.sudoku_id).first()
        data.append([sudoku.id, sudoku.difficulty, str(sudoku.created_at)[:19], user_sudoku.time, str(user_sudoku.started_at)[:19], str(user_sudoku.last_saved)[:19]])

    session.close()
    return data

def check_win(sudoku):
    """
    Checks if a Sudoku puzzle is completely solved.

    Args:
    - sudoku (object): Sudoku object containing cells and squares.

    Returns:
    - bool: True if the Sudoku puzzle is solved, False otherwise.
    """
    right = 0
    for i in range(9):
        square_row = i // 3
        square_column = i % 3
        square = sudoku.squares[f'square_{square_row}_{square_column}']
        if square.check_square_for_win() and check_row_for_win(sudoku, i) and check_column_for_win(sudoku, i):
            right += 1
    return right == 9

def check_row_for_win(sudoku, row):
    """
    Checks if a specific row in a Sudoku puzzle contains all numbers from 1 to 9.

    Args:
    - sudoku (object): Sudoku object containing cells.
    - row (int): Row index to be checked.

    Returns:
    - bool: True if the row contains all numbers from 1 to 9, False otherwise.
    """
    numbers = []
    for i in range(9):
        cell = sudoku.cells[f'cell_{row}_{i}']
        if cell.text():
            numbers.append(cell.text())
        
    if len(set(numbers)) == 9:
        return True
    return False

def check_column_for_win(sudoku, column):
    """
    Checks if a specific column in a Sudoku puzzle contains all numbers from 1 to 9.

    Args:
    - sudoku (object): Sudoku object containing cells.
    - column (int): Column index to be checked.

    Returns:
    - bool: True if the column contains all numbers from 1 to 9, False otherwise.
    """
    numbers = []
    for i in range(9):
        cell = sudoku.cells[f'cell_{i}_{column}']
        if cell.text():
            numbers.append(cell.text())
        
    if len(set(numbers)) == 9:
        return True
    return False

def is_valid(sudoku_string):
    """
    Validates if a Sudoku puzzle string representation is valid.

    Args:
    - sudoku_string (str): String representation of a Sudoku puzzle.

    Returns:
    - bool: True if the Sudoku puzzle string is valid, False otherwise.
    """
    sudoku = sudoku_string.split(',')

    print("Checking if the number of numbers is bigger than 81")
    if len(sudoku) != 81:
        return False
    
    print("Checking if the numbers are valid")
    for digit in sudoku:
        if not digit.isdigit() or int(digit) < 0 or int(digit) > 9:
            return False
    return True

def is_solvable(sudoku_string):
    """
    Determines if a Sudoku puzzle string representation is solvable.

    Args:
    - sudoku_string (str): String representation of a Sudoku puzzle.

    Returns:
    - bool: True if the Sudoku puzzle is solvable, False otherwise.
    """
    sudoku = sudoku_string.split(',')
    
    print("Checking if the number of numbers is bigger than 17")
    if sudoku.count('0') > 64:
        return False
    
    sudoku_grid = [sudoku[i:i+9] for i in range(0, len(sudoku), 9)]

    for row in sudoku_grid:
        print(row)

    print("Checking if rows are valid")
    for row in sudoku_grid:
        temp = [int(i) for i in row if i != '0']
        if len(temp) != len(set(temp)):
            print("Invalid row", row)
            return False
    
    print("Checking if columns are valid")
    for i in range(9):
        column = [row[i] for row in sudoku_grid]

        temp = [int(i) for i in column if i != '0']
        if len(temp) != len(set(temp)):
            return False

    print("Checking if squares are valid")
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            square = [sudoku_grid[x][y] for x in range(i, i+3) for y in range(j, j+3)]

            temp = [int(i) for i in square if i != '0']
            if len(temp) != len(set(temp)):
                return False
    
    return True

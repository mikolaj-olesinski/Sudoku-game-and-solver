from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import UsersSudoku_model, Sudoku_model, User_model
from model.utils.classes import BlankCell, ComputerCell, SolvedCell
import random, re

def get_board_from_file(filename):
    with open(filename, 'r') as file:
        content = file.read().replace('\n', '').split(',')

    board = {}
    for i in range(9):
        for j in range(9):
            board[f'cell_{i}_{j}'] = content[i * 9 + j]

    return board

def get_board_from_db(sudoku_id, user_id):

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

def get_data_from_sudoku(sudoku):
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
    for i in range(9):
        if grid[r][i] == k:
            return False
    
    for i in range(9):
        if grid[i][c] == k:
            return False
    
    startRow, startCol = 3 * (r // 3), 3 * (c // 3)
    for i in range(3):
        for j in range(3):
            if grid[startRow + i][startCol + j] == k:
                return False
    
    return True

def solve_sudoku(grid, r=0, c=0, steps=None):
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
    if isSolved:
        return rate_difficulty(steps)
    else:
        return "Unsolvable"
    
def get_hint_for_sudoku(data, solved):
    empty_positions = [(i, j) for i in range(9) for j in range(9) if data[i][j] == 0]

    if not empty_positions:
        return None

    i, j = random.choice(empty_positions)
    return i, j, solved[i][j]

def flatten_to_string(lst):
    flattened = [str(item) for sublist in lst for item in sublist]
    return ','.join(flattened)

def databaseData_to_grid(string):
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
    if len(username) > 15 or len(username) < 3:
        print('Username must be between 3 and 15 characters')
        return False

    if not re.match("^[a-zA-Z0-9]*$", username):
        print('Username must contain only letters and numbers')
        return False

    print('Username is valid')
    return True

def get_sudoku_string_from_file(filename):

    with open(filename, 'r') as file:
        content = file.read().replace('\n', '').split(',')

    string = ",".join(content)
    return string

def import_data_from_db(user_id):
    db_name = 'sudoku_database'
    engine = create_engine(f'sqlite:///database/{db_name}.sqlite3')

    Session = sessionmaker(bind=engine)
    session = Session()
    
    users_sudoku = session.query(UsersSudoku_model).filter(UsersSudoku_model.user_id == user_id).all()

    data = []
    for user_sudoku in users_sudoku:
        sudoku = session.query(Sudoku_model).filter(Sudoku_model.id == user_sudoku.sudoku_id).first()
        data.append([sudoku.id, sudoku.difficulty, user_sudoku.is_solved, user_sudoku.time, str(user_sudoku.started_at)[:19], str(user_sudoku.last_saved)[:19]])

    session.close()
    return data
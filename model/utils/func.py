from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Sudoku_model
import random

def get_board_from_file(filename):
    with open(filename, 'r') as file:
        content = file.read().replace('\n', '').split(',')

    board = {}
    for i in range(9):
        for j in range(9):
            board[f'cell_{i}_{j}'] = content[i * 9 + j]

    return board

def get_board_from_db(sudoku_id):
    db_name = 'sudoku_database'
    engine = create_engine(f'sqlite:///database/{db_name}.sqlite3')

    Session = sessionmaker(bind=engine)
    session = Session()

    sudoku = session.query(Sudoku_model).filter(Sudoku_model.id == sudoku_id).first()
    data = sudoku.data.split(',')
    board = {}
    for i in range(9):
        for j in range(9):
            board[f'cell_{i}_{j}'] = data[i * 9 + j]

    session.close()
    return board, sudoku_id

def get_data_from_sudoku(sudoku):
    cells = sudoku.cells
    string = ''

    for i in range(9):
        for j in range(9):
            if cells[f"cell_{i}_{j}"].text():
                string += f'{cells[f"cell_{i}_{j}"].text()},'
            else:
                string += '0,'
    return string
    
def isValid(grid, r, c, k):
    for i in range(9):
        if grid[r][i] == k or grid[i][c] == k:
            return False
    for i in range(3):
        for j in range(3):
            if grid[r + i][c + j] == k:
                return False
    return True

def isValid(grid, r, c, k):
    # Sprawdzenie wiersza
    for i in range(9):
        if grid[r][i] == k:
            return False
    
    # Sprawdzenie kolumny
    for i in range(9):
        if grid[i][c] == k:
            return False
    
    # Sprawdzenie 3x3 kwadratu
    startRow, startCol = 3 * (r // 3), 3 * (c // 3)
    for i in range(3):
        for j in range(3):
            if grid[startRow + i][startCol + j] == k:
                return False
    
    return True

def solve_sudoku(grid, r=0, c=0):
    if r == 9:
        return True
    if c == 9:
        return solve_sudoku(grid, r + 1, 0)
    if grid[r][c] != 0:
        return solve_sudoku(grid, r, c + 1)
    else:
        for k in range(1, 10):
            if isValid(grid, r, c, k):
                grid[r][c] = k
                if solve_sudoku(grid, r, c + 1):
                    return True
                grid[r][c] = 0
        return False
    
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


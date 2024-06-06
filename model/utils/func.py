from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model.database.models import Sudoku_model

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
    engine = create_engine(f'sqlite:///model/database/{db_name}.sqlite3')

    Session = sessionmaker(bind=engine)
    session = Session()

    sudoku = session.query(Sudoku_model).filter(Sudoku_model.id == sudoku_id).first()
    data = sudoku.data.split(',')
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
    



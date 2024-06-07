import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Sudoku_model, User_model, UsersSudoku_model
from model.utils.func import solve_sudoku, databaseData_to_grid, flatten_to_string, find_difficulty, sudoku_data_to_users_sudoku_data


def addSudoku(data):
    sudoku = Sudoku_model(data=data, created_at=datetime.now())
    
    grid = databaseData_to_grid(data)
    isSolved, steps = solve_sudoku(grid)
    grid = flatten_to_string(grid)

    sudoku.difficulty = find_difficulty(isSolved, steps)
    sudoku.solved_data = grid

    session.add(sudoku)
    session.commit()

def addUser(name):
    user = User_model(name=name, created_at=datetime.now())
    session.add(user)
    session.commit()

def addUsersSudoku(user_id, sudoku_id, started_at, last_saved, time, is_solved):
    sudoku = session.query(Sudoku_model).filter(Sudoku_model.id == sudoku_id).first()
    user = session.query(User_model).filter(User_model.id == user_id).first()
    users_sudoku = UsersSudoku_model(user_id=user.id, sudoku_id=sudoku.id, started_at=started_at, last_saved=last_saved, time=time, is_solved=is_solved)
    users_sudoku.current_sudoku_state = sudoku_data_to_users_sudoku_data(sudoku.data)
    session.add(users_sudoku)
    session.commit()

if __name__ == '__main__':
    db_name = 'sudoku_database'
    engine = create_engine(f'sqlite:///database/{db_name}.sqlite3')

    Session = sessionmaker(bind=engine)
    session = Session()

    sudoku_data = "0,7,0,5,8,3,0,2,0," \
                "0,5,9,2,0,0,3,0,0," \
                "3,4,0,0,0,6,5,0,7," \
                "0,0,3,6,9,7,1,0,0," \
                "7,9,5,0,0,0,6,3,2," \
                "6,8,0,0,0,2,7,0,0," \
                "9,1,4,8,3,5,0,7,6," \
                "0,3,0,7,0,1,4,9,5," \
                "5,6,7,4,2,9,0,1,3"

    addSudoku(data=sudoku_data)

    addUser(name='test')

    addUsersSudoku(user_id=1, sudoku_id=1, started_at=datetime.now(), last_saved=datetime.now(), time=0, is_solved=False)

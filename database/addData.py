import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Sudoku_model, User_model, UsersSudoku_model
from model.utils.func import solve_sudoku, databaseData_to_grid, flatten_to_string



def addSudoku(data, created_at):
    sudoku = Sudoku_model(data=data, created_at=created_at)
    grid = databaseData_to_grid(data)
    solve_sudoku(grid)
    grid = flatten_to_string(grid)
    
    sudoku.solved = grid
    session.add(sudoku)
    session.commit()

def addUser(name, created_at):
    user = User_model(name=name, created_at=created_at)
    session.add(user)
    session.commit()

def addUsersSudoku(sudoku_name, user_name, started_at, finished_at=None, time=None, cuurent_sudoku_state=None):
    sudoku = session.query(Sudoku_model).filter(Sudoku_model.name == sudoku_name).first()
    user = session.query(User_model).filter(User_model.name == user_name).first()
    users_sudoku = UsersSudoku_model(user_id=user.id, sudoku_id=sudoku.id, started_at=started_at, finished_at=finished_at, time=time, cuurent_sudoku_state=cuurent_sudoku_state)
    session.add(users_sudoku)
    session.commit()

if __name__ == '__main__':
    db_name = 'sudoku_database'
    engine = create_engine(f'sqlite:///database/{db_name}.sqlite3')

    Session = sessionmaker(bind=engine)
    session = Session()

    sudoku_data = "0,C7,0,C5,C8,C3,0,C2,0," \
                "0,C5,C9,C2,0,0,C3,0,0," \
                "C3,C4,0,0,0,C6,C5,0,C7," \
                "0,0,C3,C6,C9,C7,C1,0,0," \
                "C7,C9,C5,0,0,0,C6,C3,C2," \
                "C6,C8,0,0,0,C2,C7,0,0," \
                "C9,C1,C4,C8,C3,C5,0,C7,C6," \
                "0,C3,0,C7,0,C1,C4,C9,C5," \
                "C5,C6,C7,C4,C2,C9,0,C1,C3"

    addSudoku(sudoku_data, datetime.now())


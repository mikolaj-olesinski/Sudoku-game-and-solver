import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from database.models import Sudoku_model, User_model, UsersSudoku_model
from model.utils.func import solve_sudoku, databaseData_to_grid, flatten_to_string, find_difficulty, sudoku_data_to_saved_sudoku_data


db_name = 'sudoku_database'
engine = create_engine(f'sqlite:///database/{db_name}.sqlite3')

Session = sessionmaker(bind=engine)
session = Session()


def addSudoku(data):
    sudoku = Sudoku_model(data=data, created_at=datetime.now())
    
    grid = databaseData_to_grid(data)
    isSolved, steps = solve_sudoku(grid)
    grid = flatten_to_string(grid)

    sudoku.difficulty = find_difficulty(isSolved, steps)
    sudoku.solved_data = grid

    session.add(sudoku)
    session.commit()

    addSudokuToAllUsers(sudoku.id)
    session.commit()

def addUser(name):
    user = User_model(name=name, created_at=datetime.now())

    session.add(user)
    session.commit()

    addToUserAllSudokus(user.id)
    session.commit()

def addUsersSudoku(user_id, sudoku_id, started_at, last_saved, time, is_solved):
    sudoku_model = session.query(Sudoku_model).filter(Sudoku_model.id == sudoku_id).first()
    user_model = session.query(User_model).filter(User_model.id == user_id).first()
    users_sudoku = UsersSudoku_model(user_id=user_model.id, sudoku_id=sudoku_model.id, started_at=started_at, last_saved=last_saved, time=time, is_solved=is_solved)
    users_sudoku.current_sudoku_state = sudoku_data_to_saved_sudoku_data(sudoku_model.data)

    session.add(users_sudoku)
    addSudokuToAllUsers(sudoku_model)
    session.commit()

def addSudokuToAllUsers(sudoku_id):
    users = session.query(User_model).all()
    sudoku_model = session.query(Sudoku_model).filter(Sudoku_model.id == sudoku_id).first()
    if users:
        for user in users:
            users_sudoku = UsersSudoku_model(user_id=user.id, sudoku_id=sudoku_model.id, started_at=datetime.now(), last_saved=datetime.now(), time=0, is_solved=False)
            users_sudoku.current_sudoku_state = sudoku_data_to_saved_sudoku_data(sudoku_model.data)

            session.add(users_sudoku)
            session.commit()
    else:
        print("No users in database")

def addToUserAllSudokus(user_id):
    sudokus = session.query(Sudoku_model).all()
    user_model = session.query(User_model).filter(User_model.id == user_id).first()
    if sudokus:
        for sudoku in sudokus:
            users_sudoku = UsersSudoku_model(user_id=user_model.id, sudoku_id=sudoku.id, started_at=datetime.now(), last_saved=datetime.now(), time=0, is_solved=False)
            users_sudoku.current_sudoku_state = sudoku_data_to_saved_sudoku_data(sudoku.data)
            session.add(users_sudoku)
            session.commit()
    else:
        print("No sudokus in database")



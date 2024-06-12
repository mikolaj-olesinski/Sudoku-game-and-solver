from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import UsersSudoku_model, User_model


db_name = 'sudoku_database'
engine = create_engine(f'sqlite:///database/{db_name}.sqlite3')

Session = sessionmaker(bind=engine)
session = Session()

def get_timer(user_id, sudoku_id):
    users_sudoku = session.query(UsersSudoku_model).filter(UsersSudoku_model.user_id == user_id, UsersSudoku_model.sudoku_id == sudoku_id).first()
    return str(users_sudoku.time)

def get_is_solved(user_id, sudoku_id):
    users_sudoku = session.query(UsersSudoku_model).filter(UsersSudoku_model.user_id == user_id, UsersSudoku_model.sudoku_id == sudoku_id).first()
    return users_sudoku.is_solved

def get_username_from_id(user_id):
    user = session.query(User_model).filter(User_model.id == user_id).first()
    return user.name


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import UsersSudoku_model


db_name = 'sudoku_database'
engine = create_engine(f'sqlite:///database/{db_name}.sqlite3')

Session = sessionmaker(bind=engine)
session = Session()


def deleteUsersSudoku(user_id, sudoku_id):
    users_sudoku = session.query(UsersSudoku_model).filter(UsersSudoku_model.user_id == user_id).filter(UsersSudoku_model.sudoku_id == sudoku_id).first()
    session.delete(users_sudoku)
    session.commit()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import UsersSudoku_model

# Database connection setup
db_name = 'sudoku_database'
engine = create_engine(f'sqlite:///database/{db_name}.sqlite3')

Session = sessionmaker(bind=engine)
session = Session()

def deleteUsersSudoku(user_id, sudoku_id):
    """
    Deletes a specific user's record of a Sudoku puzzle from the database.

    Parameters
    ----------
    user_id : int
        The ID of the user whose Sudoku puzzle record is to be deleted.
    sudoku_id : int
        The ID of the Sudoku puzzle to be deleted from the user's records.

    """
    users_sudoku = session.query(UsersSudoku_model).filter(UsersSudoku_model.user_id == user_id).filter(UsersSudoku_model.sudoku_id == sudoku_id).first()
    session.delete(users_sudoku)
    session.commit()

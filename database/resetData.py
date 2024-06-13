from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Sudoku_model, UsersSudoku_model
from model.utils.func import sudoku_data_to_saved_sudoku_data


db_name = 'sudoku_database'
engine = create_engine(f'sqlite:///database/{db_name}.sqlite3')

Session = sessionmaker(bind=engine)
session = Session()

def resetUsersSudoku(user_id, sudoku_id):
    """
    Resets the state of a user's Sudoku puzzle.

    Parameters
    ----------
    user_id : int
        The ID of the user.
    sudoku_id : int
        The ID of the Sudoku puzzle to be reset.

    """
    # Resetting UsersSudoku_model attributes
    users_sudoku = session.query(UsersSudoku_model).filter(
        UsersSudoku_model.user_id == user_id,
        UsersSudoku_model.sudoku_id == sudoku_id
    ).first()
    
    users_sudoku.last_saved = None
    users_sudoku.time = "00:00:00"
    users_sudoku.is_solved = False

    # Updating current_sudoku_state based on original Sudoku data
    sudoku_model = session.query(Sudoku_model).filter(Sudoku_model.id == sudoku_id).first()
    users_sudoku.current_sudoku_state = sudoku_data_to_saved_sudoku_data(sudoku_model.data)

    session.commit()

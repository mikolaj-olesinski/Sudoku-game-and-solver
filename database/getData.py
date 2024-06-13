from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import UsersSudoku_model, User_model

# Database connection setup
db_name = 'sudoku_database'
engine = create_engine(f'sqlite:///database/{db_name}.sqlite3')

Session = sessionmaker(bind=engine)
session = Session()

def get_timer(user_id, sudoku_id):
    """
    Retrieves the timer value (time spent) for a specific user and Sudoku puzzle.

    Parameters
    ----------
    user_id : int
        The ID of the user.
    sudoku_id : int
        The ID of the Sudoku puzzle.

    Returns
    -------
    str
        The string representation of the time spent on the Sudoku puzzle.

    """
    users_sudoku = session.query(UsersSudoku_model).filter(UsersSudoku_model.user_id == user_id, UsersSudoku_model.sudoku_id == sudoku_id).first()
    return str(users_sudoku.time)

def get_is_solved(user_id, sudoku_id):
    """
    Checks if a specific Sudoku puzzle is solved for a given user.

    Parameters
    ----------
    user_id : int
        The ID of the user.
    sudoku_id : int
        The ID of the Sudoku puzzle.

    Returns
    -------
    bool
        True if the Sudoku puzzle is solved for the user, False otherwise.

    """
    users_sudoku = session.query(UsersSudoku_model).filter(UsersSudoku_model.user_id == user_id, UsersSudoku_model.sudoku_id == sudoku_id).first()
    return users_sudoku.is_solved

def get_username_from_id(user_id):
    """
    Retrieves the username associated with a given user ID.

    Parameters
    ----------
    user_id : int
        The ID of the user.

    Returns
    -------
    str
        The username corresponding to the user ID.

    """
    user = session.query(User_model).filter(User_model.id == user_id).first()
    return user.name

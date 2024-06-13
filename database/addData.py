from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from database.models import Sudoku_model, User_model, UsersSudoku_model
from model.utils.func import solve_sudoku, databaseData_to_grid, flatten_to_string, find_difficulty, sudoku_data_to_saved_sudoku_data

# Database connection setup
db_name = 'sudoku_database'
engine = create_engine(f'sqlite:///database/{db_name}.sqlite3')

Session = sessionmaker(bind=engine)
session = Session()


def addSudoku(data):
    """
    Adds a new Sudoku puzzle to the database.

    This function creates a new Sudoku_model instance with provided data, solves the Sudoku to determine its difficulty,
    and stores the solved state in the database.

    Parameters
    ----------
    data : str
        The Sudoku puzzle data in string format.

    """
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
    """
    Adds a new user to the database.

    This function creates a new User_model instance with the provided username and stores it in the database.

    Parameters
    ----------
    name : str
        The username to be added to the database.

    """
    user = User_model(name=name, created_at=datetime.now())

    session.add(user)
    session.commit()

    addToUserAllSudokus(user.id)
    session.commit()


def addUsersSudoku(user_id, sudoku_id, started_at, last_saved, time, is_solved):
    """
    Adds a Sudoku puzzle to a specific user's list of puzzles in the database.

    Parameters
    ----------
    user_id : int
        The ID of the user.
    sudoku_id : int
        The ID of the Sudoku puzzle.
    started_at : datetime
        The timestamp when the user started the Sudoku puzzle.
    last_saved : datetime
        The timestamp when the Sudoku puzzle was last saved by the user.
    time : str
        The time spent by the user on the Sudoku puzzle.
    is_solved : bool
        Indicates if the Sudoku puzzle is solved or not.

    """
    sudoku_model = session.query(Sudoku_model).filter(Sudoku_model.id == sudoku_id).first()

    users_sudoku = UsersSudoku_model(user_id=user_id, sudoku_id=sudoku_model.id, started_at=started_at, last_saved=last_saved, time=time, is_solved=is_solved)
    users_sudoku.current_sudoku_state = sudoku_data_to_saved_sudoku_data(sudoku_model.data)

    session.add(users_sudoku)
    addSudokuToAllUsers(sudoku_model)
    session.commit()


def addSudokuToAllUsers(sudoku_id):
    """
    Adds a Sudoku puzzle to all users in the database.

    Parameters
    ----------
    sudoku_id : int
        The ID of the Sudoku puzzle to be added to all users.

    """
    users = session.query(User_model).all()
    sudoku_model = session.query(Sudoku_model).filter(Sudoku_model.id == sudoku_id).first()
    
    if users:
        for user in users:
            users_sudoku = UsersSudoku_model(user_id=user.id, sudoku_id=sudoku_model.id, started_at=None, last_saved=None, time="00:00:00", is_solved=False)
            users_sudoku.current_sudoku_state = sudoku_data_to_saved_sudoku_data(sudoku_model.data)

            session.add(users_sudoku)
            session.commit()
    else:
        print("No users in database")


def addToUserAllSudokus(user_id):
    """
    Adds all Sudoku puzzles to a specific user in the database.

    Parameters
    ----------
    user_id : int
        The ID of the user to whom all Sudoku puzzles are to be added.

    """
    sudokus = session.query(Sudoku_model).all()
    
    if sudokus:
        for sudoku in sudokus:
            users_sudoku = UsersSudoku_model(user_id=user_id, sudoku_id=sudoku.id, started_at=None, last_saved=None, time="00:00:00", is_solved=False)
            users_sudoku.current_sudoku_state = sudoku_data_to_saved_sudoku_data(sudoku.data)
            session.add(users_sudoku)
            session.commit()
    else:
        print("No sudokus in database")


def addTimer(user_id, sudoku_id, time):
    """
    Updates the time spent on a specific Sudoku puzzle by a user in the database.

    Parameters
    ----------
    user_id : int
        The ID of the user.
    sudoku_id : int
        The ID of the Sudoku puzzle.
    time : str
        The time spent on the Sudoku puzzle.

    """
    user_sudoku = session.query(UsersSudoku_model).filter(UsersSudoku_model.user_id == user_id, UsersSudoku_model.sudoku_id == sudoku_id).first()
    user_sudoku.time = time
    session.commit()


def addSolvedSudoku(user_id, sudoku_id):
    """
    Marks a specific Sudoku puzzle as solved by a user in the database.

    Parameters
    ----------
    user_id : int
        The ID of the user.
    sudoku_id : int
        The ID of the Sudoku puzzle.

    """
    user_sudoku = session.query(UsersSudoku_model).filter(UsersSudoku_model.user_id == user_id, UsersSudoku_model.sudoku_id == sudoku_id).first()
    user_sudoku.is_solved = True
    print(user_sudoku.is_solved)
    session.commit()

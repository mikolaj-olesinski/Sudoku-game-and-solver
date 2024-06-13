from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Sudoku_model(Base):
    """
    Represents a Sudoku puzzle in the database.

    Attributes
    ----------
    id : int
        Primary key identifying the Sudoku puzzle.
    created_at : DateTime
        Timestamp indicating when the Sudoku puzzle was created.
    data : str
        String representation of the initial state of the Sudoku puzzle.
    solved_data : str
        String representation of the solved state of the Sudoku puzzle.
    difficulty : str
        String representing the difficulty level of the Sudoku puzzle.

    """
    __tablename__ = 'sudoku'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    data = Column(String)
    solved_data = Column(String)
    difficulty = Column(String)


class User_model(Base):
    """
    Represents a user in the database.

    Attributes
    ----------
    id : int
        Primary key identifying the user.
    name : str
        The username of the user.
    created_at : DateTime
        Timestamp indicating when the user account was created.

    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime)


class UsersSudoku_model(Base):
    """
    Represents the relationship between users and Sudoku puzzles in the database.

    Attributes
    ----------
    user_id : int
        Foreign key referencing the user associated with the Sudoku puzzle.
    sudoku_id : int
        Foreign key referencing the Sudoku puzzle.
    started_at : DateTime
        Timestamp indicating when the user started solving the Sudoku puzzle.
    last_saved : DateTime
        Timestamp indicating when the Sudoku puzzle was last saved by the user.
    time : int
        Integer representing the time spent by the user on the Sudoku puzzle.
    is_solved : bool
        Boolean indicating if the Sudoku puzzle is solved by the user.
    current_sudoku_state : str
        String representation of the current state of the Sudoku puzzle as seen by the user.

    """
    __tablename__ = 'users_sudoku'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    sudoku_id = Column(Integer, ForeignKey('sudoku.id'), primary_key=True)
    started_at = Column(DateTime)
    last_saved = Column(DateTime)
    time = Column(Integer)
    is_solved = Column(Boolean)
    current_sudoku_state = Column(String)

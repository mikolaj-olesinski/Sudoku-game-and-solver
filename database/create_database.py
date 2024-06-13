import sys
import os
from sqlalchemy import create_engine
from database.models import Base
from database.addData import addSudoku, addUser
from model.utils.func import get_sudoku_string_from_file

def create_database(db_name):
    """
    Creates a SQLite database if it does not already exist.

    Parameters
    ----------
    db_name : str
        The name of the database to be created.

    """
    database_path = f'database/{db_name}.sqlite3'

    if os.path.exists(database_path):
        pass
    else:
        engine = create_engine(f'sqlite:///{database_path}')
        Base.metadata.create_all(engine)
        print(f'Database {db_name} created')


def create_database_and_add_basic_sudokus(db_name):
    """
    Creates a SQLite database if it does not already exist and adds basic Sudoku puzzles.

    Parameters
    ----------
    db_name : str
        The name of the database to be created and populated with basic Sudoku puzzles.

    """
    database_path = f'database/{db_name}.sqlite3'

    if os.path.exists(database_path):
        pass
    else:
        engine = create_engine(f'sqlite:///{database_path}')
        Base.metadata.create_all(engine)
        print(f'Database {db_name} created')

        sudoku1 = get_sudoku_string_from_file("constants/sudoku1.txt")
        sudoku2 = get_sudoku_string_from_file("constants/sudoku2.txt")
        sudoku3 = get_sudoku_string_from_file("constants/sudoku3.txt")
        sudoku4 = get_sudoku_string_from_file("constants/sudoku4.txt")
        sudoku5 = get_sudoku_string_from_file("constants/sudoku5.txt")
        sudoku6 = get_sudoku_string_from_file("constants/sudoku6.txt")

        addUser("admin")
        addSudoku(sudoku1)
        addSudoku(sudoku2)
        addSudoku(sudoku3)
        addSudoku(sudoku4)
        addSudoku(sudoku5)
        addSudoku(sudoku6)

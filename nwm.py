from PySide6.QtGui import QValidator
from PySide6.QtWidgets import QLineEdit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dataBase.models import Sudoku, User, UsersSudoku, Base

class NonZeroValidator(QValidator):
    def validate(self, input_str, pos):
        if not input_str:
            return (QValidator.Acceptable, input_str, pos)
        try:
            value = int(input_str)
            if value != 0:
                return (QValidator.Acceptable, input_str, pos)
            else:
                return (QValidator.Invalid, input_str, pos)
        except ValueError:
            return (QValidator.Invalid, input_str, pos)
        

class UserCell(QLineEdit):
    def __init__(self):
        super().__init__()

    def copy_properties(self, other):
        self.setObjectName(other.objectName())
        self.setAlignment(other.alignment())
        self.setFixedSize(other.size())
        self.setValidator(other.validator())
        self.setMaxLength(other.maxLength())

class ComputerCell(QLineEdit):
    def __init__(self):
        super().__init__()

    def copy_properties(self, other):
        self.setObjectName(other.objectName())
        self.setAlignment(other.alignment())
        self.setFixedSize(other.size())
        self.setValidator(other.validator())
        self.setMaxLength(other.maxLength())

class BlankCell(QLineEdit):
    def __init__(self):
        super().__init__()

    def copy_properties(self, other):
        self.setObjectName(other.objectName())
        self.setAlignment(other.alignment())
        self.setFixedSize(other.size())
        self.setValidator(other.validator())
        self.setMaxLength(other.maxLength())





def get_board_from_file(filename):
    with open(filename, 'r') as file:
        content = file.read().replace('\n', '').split(',')

    board = {}
    for i in range(9):
        for j in range(9):
            board[f'cell_{i}_{j}'] = content[i * 9 + j]

    return board

def get_board_from_db(sudoku_id):
    db_name = 'sudoku_database'
    engine = create_engine(f'sqlite:///dataBase/{db_name}.sqlite3')

    Session = sessionmaker(bind=engine)
    session = Session()

    sudoku = session.query(Sudoku).filter(Sudoku.id == sudoku_id).first()
    data = sudoku.data.split(',')
    board = {}
    for i in range(9):
        for j in range(9):
            board[f'cell_{i}_{j}'] = data[i * 9 + j]

    session.close()
    return board

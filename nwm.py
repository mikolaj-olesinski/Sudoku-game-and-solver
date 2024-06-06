from PySide6.QtGui import QValidator
from PySide6.QtWidgets import QLineEdit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QHBoxLayout
from PySide6.QtCore import QTimer, Qt
from dataBase.models import Sudoku

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
        self.setText(other.text())

class ComputerCell(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('color: #ddd;')
        self.setReadOnly(True)

    def copy_properties(self, other):
        self.setObjectName(other.objectName())
        self.setAlignment(other.alignment())
        self.setFixedSize(other.size())
        self.setValidator(other.validator())
        self.setMaxLength(other.maxLength())

class BlankCell(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('color: #458;')
        #self.setCursor(Qt.ArrowCursor)

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

def get_data_from_sudoku(sudoku):
    cells = sudoku.cells
    string = ''

    for i in range(9):
        for j in range(9):
            string += f'{cells[i][j].text()},'
    

class Stoper(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.time_label = QLabel("00:00:00", self)
        self.time_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.time_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        self.elapsed_time = 0

        self.start_timer()  # Automatyczne rozpoczęcie timera po uruchomieniu

    def start_timer(self):
        self.timer.start(1000)  # Aktualizacja co 1 sekunda

    def update_time(self):
        self.elapsed_time += 1
        hours, remainder = divmod(self.elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.time_label.setText(f"{hours:02}:{minutes:02}:{seconds:02}")


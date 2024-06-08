from PySide6.QtWidgets import QApplication, QTableView, QWidget, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Sudoku_model, User_model, UsersSudoku_model

class SudokuPicker(QTableView):
    def __init__(self, data=None):
        super().__init__()
        if data is not None:
            model = SudokuModel(data)
            self.setModel(model)
            self.setSortingEnabled(True)

    def import_data_from_db(self, username):
        db_name = 'sudoku_database'
        engine = create_engine(f'sqlite:///database/{db_name}.sqlite3')

        Session = sessionmaker(bind=engine)
        session = Session()

        user_id = session.query(User_model).filter(User_model.name == username).first().id
        users_sudoku = session.query(UsersSudoku_model).filter(UsersSudoku_model.user_id == user_id).all()

        data = []
        for user_sudoku in users_sudoku:
            sudoku = session.query(Sudoku_model).filter(Sudoku_model.id == user_sudoku.sudoku_id).first()
            data.append([sudoku.id, sudoku.difficulty, user_sudoku.is_solved, user_sudoku.time, str(user_sudoku.started_at)[:19], str(user_sudoku.last_saved)[:19]])
        
        model = SudokuModel(data)
        self.setModel(model)

class SudokuModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0])

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return ['id', 'difficulty', 'solved', 'timer', 'started_at', 'last_saved'][section]


if __name__ == "__main__":
    app = QApplication([])

    sudoku_picker = SudokuPicker()
    sudoku_picker.import_data_from_db('admin')
    sudoku_picker.show()

    app.exec()

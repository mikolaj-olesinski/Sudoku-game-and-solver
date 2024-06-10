from PySide6.QtWidgets import QTableView, QStyledItemDelegate, QWidget, QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QMouseEvent
from model.utils.func import import_data_from_db
from PySide6.QtGui import QPixmap
from controller.apps.sudoku_game_app import sudoku_app
from database.deleteData import deleteUsersSudoku
from database.resetData import resetUsersSudoku
import os

class SudokuModel(QAbstractTableModel):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.sudoku_data = import_data_from_db(user_id)

    def rowCount(self, parent=QModelIndex()):
        return len(self.sudoku_data)

    def columnCount(self, parent=QModelIndex()):
        return len(self.sudoku_data[0]) + 4

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if index.column() < 6: 
                return self.sudoku_data[index.row()][index.column()]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                headers = ['id', 'difficulty', 'solved', 'timer', 'started_at', 'last_saved', 'Start', 'Edit', 'Reset', 'Delete']
                return headers[section]

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        if column < 6:
            self.sudoku_data.sort(key=lambda x: x[column], reverse=order == Qt.DescendingOrder)
        self.layoutChanged.emit()
    
    def update_data(self):
        self.sudoku_data = import_data_from_db(self.user_id)
        self.layoutChanged.emit()


class ButtonDelegate(QStyledItemDelegate):
    def __init__(self, sudoku_picker, parent=None):
        super().__init__(parent)
        self.sudoku_picker = sudoku_picker

    def paint(self, painter, option, index):
        if index.column() >= 6:
            self._drawButton(painter, option, index)
        else:
            super().paint(painter, option, index)

    def editorEvent(self, event, model, option, index):
        if event.type() == QMouseEvent.MouseButtonRelease and index.column() == 6:
            self._handleStartButtonClick(model, index)
        elif event.type() == QMouseEvent.MouseButtonRelease and index.column() == 7:
            self._handleEditButtonClick(model, index)
        elif event.type() == QMouseEvent.MouseButtonRelease and index.column() == 8:
            self._handleResetButtonClick(model, index)
        elif event.type() == QMouseEvent.MouseButtonRelease and index.column() == 9:
            self._handleDeleteButtonClick(model, index)
        return super().editorEvent(event, model, option, index)

    def get_path_for_icon(self, index):
        base_path = os.path.abspath(os.path.join("constants", "resources"))
        icons = ["play.png", "edit.png", "reset.png", "delete.png"]
        if 6 <= index.column() <= 9:
            return os.path.join(base_path, icons[index.column() - 6])
        return "Button"

    def _drawButton(self, painter, option, index):
        button_rect = option.rect
        sudoku_data = self.get_path_for_icon(index)
        if sudoku_data and os.path.isfile(sudoku_data):
            button_icon = QPixmap(sudoku_data)
            button_icon = button_icon.scaled(button_rect.size(), Qt.KeepAspectRatio)
            button_icon_rect = button_icon.rect()
            button_icon_rect.moveCenter(button_rect.center())
            painter.drawPixmap(button_icon_rect, button_icon)
        else:
            button_text = sudoku_data if isinstance(sudoku_data, str) else 'Button'
            painter.drawText(button_rect, Qt.AlignCenter, button_text)

    def _handleStartButtonClick(self, model, index):
        dane = model.sudoku_data[index.row()]
        sudoku_id = dane[0]
        self.sudoku_picker.open_sudoku(sudoku_id)

    def _handleEditButtonClick(self, model, index):
        pass

    def _handleResetButtonClick(self, model, index):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Potwierdzenie")
        msg_box.setText("Czy na pewno chcesz resetowac?")
        
        yes_button = msg_box.addButton("Tak", QMessageBox.YesRole)
        no_button = msg_box.addButton("Nie", QMessageBox.NoRole)

        msg_box.exec()

        if msg_box.clickedButton() == yes_button:
            dane = model.sudoku_data[index.row()]
            sudoku_id = dane[0]
            print(sudoku_id)
            resetUsersSudoku(self.sudoku_picker.user_id, sudoku_id)
            self.sudoku_picker.update_data()



    def _handleDeleteButtonClick(self, model, index):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setWindowTitle("Potwierdzenie")
        msg_box.setText("Czy na pewno chcesz usunac?")

        yes_button = msg_box.addButton("Tak", QMessageBox.YesRole)
        no_button = msg_box.addButton("Nie", QMessageBox.NoRole)

        msg_box.exec()

        if msg_box.clickedButton() == yes_button:
            dane = model.sudoku_data[index.row()]
            sudkou_id = dane[0]
            deleteUsersSudoku(self.sudoku_picker.user_id, sudkou_id)
            self.sudoku_picker.update_data()


class SudokuPicker(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self._setupUI()

    def _setupUI(self):
        self.layout = QVBoxLayout(self)
        self.table_view = QTableView()
        self.layout.addWidget(self.table_view)
        self._initializeModelAndView()
        self._setWindowSize()

    def _initializeModelAndView(self):
        self.model = SudokuModel(self.user_id)
        self.table_view.setModel(self.model)
        self.table_view.setSortingEnabled(True)
        self.table_view.setItemDelegate(ButtonDelegate(self))
        self.table_view.resizeColumnsToContents()

    def _setWindowSize(self):
        table_width = self.table_view.horizontalHeader().length() + 30
        self.resize(table_width, 400)

    def open_sudoku(self, sudoku_id):
        self.cams = sudoku_app(self.user_id, sudoku_id, self)
        self.cams.show()
        self.cams.setWindowTitle(f"Użytkownik: {self.user_id}")
        self.hide()

    def update_data(self):
        self.model.update_data()
        self.table_view.resizeColumnsToContents()
        self._setWindowSize()

    
    



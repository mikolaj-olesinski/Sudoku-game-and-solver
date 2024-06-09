from PySide6.QtWidgets import QApplication, QTableView, QStyledItemDelegate, QWidget, QVBoxLayout, QStyle, QStyleOptionButton
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QMouseEvent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from PySide6.QtGui import QPixmap
import os

# Przykładowe dane
sample_data = [
    [1, 'Easy', True, '00:15', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
    [2, 'Medium', False, '00:30', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
    [3, 'Hard', True, '01:00', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
    [4, 'Easy', False, '00:20', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
    [5, 'Medium', True, '00:40', datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
]


class SudokuModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._data[0]) + 4  # Add one for each button column

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if index.column() < 6:  # Display data for the first five columns
                return self._data[index.row()][index.column()]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                headers = ['id', 'difficulty', 'solved', 'timer', 'started_at', 'last_saved', 'Start', 'Edit', 'Reset', 'Delete']
                return headers[section]

    def sort(self, column, order):
        self.layoutAboutToBeChanged.emit()
        if column < 6:  # Sort only for the first five columns
            self._data.sort(key=lambda x: x[column], reverse=order == Qt.DescendingOrder)
        self.layoutChanged.emit()



class ButtonDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        if index.column() >= 6:  # Assuming the buttons start from column 6
            button_rect = option.rect
            data = self.get_path_for_icon(index)
            if data and os.path.isfile(data):  # Sprawdzanie, czy data jest ścieżką do pliku
                button_icon = QPixmap(data)
                button_icon = button_icon.scaled(button_rect.size(), Qt.KeepAspectRatio)
                button_icon_rect = button_icon.rect()
                button_icon_rect.moveCenter(button_rect.center())
                painter.drawPixmap(button_icon_rect, button_icon)
            elif isinstance(data, str):
                button_text = data
                painter.drawText(button_rect, Qt.AlignCenter, button_text)
            else: 
                button_text = 'Button'
                painter.drawText(button_rect, Qt.AlignCenter, button_text)
        else:
            super().paint(painter, option, index)

    def editorEvent(self, event, model, option, index):
        if index.column() >= 6 and event.type() == QMouseEvent.MouseButtonPress:
            data = index.data(Qt.DisplayRole)
            if data:
                print(f'Button clicked at row {index.row()} and column {index.column()} with data {data}')
            else:
                print(f'Button clicked at row {index.row()} and column {index.column()}')
            return True
        return super().editorEvent(event, model, option, index)
    
    def get_path_for_icon(self, index):
        if index.column() == 6:
            return r"constants\resources\play.png"
        elif index.column() == 7:
            return r"constants\resources\edit.png"
        elif index.column() == 8:
            return r"constants\resources\reset.png"
        elif index.column() == 9:
            return r"constants\resources\delete.png"
        else:
            return "Button"

class SudokuPicker(QWidget):
    def __init__(self, data=None):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.table_view = QTableView()
        self.layout.addWidget(self.table_view)

        if data is not None:
            self.model = SudokuModel(data)
            self.table_view.setModel(self.model)
            self.table_view.setSortingEnabled(True)
            self.table_view.setItemDelegate(ButtonDelegate())

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle('Fusion')

    sudoku_picker = SudokuPicker(sample_data)
    sudoku_picker.show()

    app.exec()

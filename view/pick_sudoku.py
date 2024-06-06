import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTableView, QVBoxLayout, QWidget,
    QPushButton, QStyledItemDelegate, QStyle, QStyleOptionButton, QMessageBox
)
from PySide6.QtCore import Qt, QModelIndex, QRect
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import QEvent


class ButtonDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        if index.column() == 3:  # Assuming the button is in the 4th column
            button = QStyleOptionButton()
            button.rect = option.rect
            button.text = "Click"
            if option.state & QStyle.State_MouseOver:
                button.state |= QStyle.State_MouseOver
            QApplication.style().drawControl(QStyle.CE_PushButton, button, painter)
        else:
            super().paint(painter, option, index)

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonRelease and index.column() == 3:
            QMessageBox.information(None, "Info", f"Button clicked at row {index.row()}")
            return True
        return super().editorEvent(event, model, option, index)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QTableView with Buttons Example")

        self.table = QTableView()

        data = [
            ["Alice", 30, "New York"],
            ["Bob", 20, "Los Angeles"],
            ["Charlie", 25, "Chicago"],
            ["David", 35, "Miami"],
        ]

        self.model = QStandardItemModel(len(data), 4)
        self.model.setHorizontalHeaderLabels(["Name", "Age", "City", "Action"])

        for row, (name, age, city) in enumerate(data):
            self.model.setItem(row, 0, QStandardItem(name))
            self.model.setItem(row, 1, QStandardItem(str(age)))
            self.model.setItem(row, 2, QStandardItem(city))
            self.model.setItem(row, 3, QStandardItem(""))

        self.table.setModel(self.model)
        self.table.setItemDelegate(ButtonDelegate())

        layout = QVBoxLayout()
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
import os
from model.sudoku_picker import SudokuPicker

class TopWidgetForSudokuPicker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(20, 20, 0, 0) 
        self.setLayout(layout)
        self.setFixedHeight(50)

        back_icon_path = os.path.abspath(os.path.join("constants", "resources", "back.png"))
        cofniecie_icon = QPixmap(back_icon_path).scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        cofniecie = QPushButton()
        cofniecie.setIcon(cofniecie_icon)
        cofniecie.setIconSize(cofniecie_icon.size())

        cofniecie.setFixedSize(cofniecie_icon.size())
        
        layout.addWidget(cofniecie, alignment=Qt.AlignLeft | Qt.AlignBottom)
        self.cofniecie = cofniecie


class BottomWidgetForSudokuPicker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(30, 0, 30, 30)
        

        add_sudoku_button = QPushButton("Dodaj sudoku")
        layout.addWidget(add_sudoku_button)
        self.add_sudoku_button = add_sudoku_button


class SudokuPickerGUI(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.initUI()
        self._setWindowSize()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.top_widget = TopWidgetForSudokuPicker()
        self.sudoku_picker = SudokuPicker(self.user_id)
        self.bottom_widget = BottomWidgetForSudokuPicker()

        main_layout.addWidget(self.top_widget)
        main_layout.addWidget(self.sudoku_picker)
        main_layout.addWidget(self.bottom_widget)

        self.setLayout(main_layout)
        self.setWindowTitle('Sudoku Application')

    def _setWindowSize(self):
        table_width = self.sudoku_picker.table_view.horizontalHeader().length() + 30
        self.setContentsMargins(0, 0, 0, 0)
        self.resize(table_width, 400)


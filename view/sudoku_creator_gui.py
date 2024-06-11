from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QApplication
from PySide6.QtGui import QPixmap
from model.utils.classes import Stoper
from model.sudoku_class import Sudoku as SudokuWidget
from PySide6.QtCore import Qt
import os

class TopWidgetForCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0) 
        self.setLayout(layout)

        back_icon_path = os.path.abspath(os.path.join("constants", "resources", "back.png"))
        cofniecie_icon = QPixmap(back_icon_path).scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        cofniecie = QPushButton()
        cofniecie.setIcon(cofniecie_icon)
        cofniecie.setIconSize(cofniecie_icon.size())

        cofniecie.setFixedSize(cofniecie_icon.size())
        
        layout.addWidget(cofniecie, alignment=Qt.AlignLeft)

        self.cofniecie = cofniecie


class BottomWidgetForCreator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        save_button = QPushButton("Zapisz")
        save_button.setObjectName("save_button")

        layout.addWidget(save_button)

        self.save_button = save_button


class SudokuCreatorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        self.top_widget = TopWidgetForCreator()
        self.sudoku = SudokuWidget()
        self.bottom_widget = BottomWidgetForCreator()

        main_layout.addWidget(self.top_widget)
        main_layout.addWidget(self.sudoku)
        main_layout.addWidget(self.bottom_widget)

        self.setLayout(main_layout)
        self.setWindowTitle('Sudoku Application')
        self.setGeometry(100, 100, 700, 600)

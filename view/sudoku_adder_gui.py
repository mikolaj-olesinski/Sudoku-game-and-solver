from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QLabel, QComboBox, QPushButton, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

class AddSudokuGUI(QMainWindow):
    """
    QMainWindow subclass representing the GUI for adding Sudoku puzzles.

    Attributes:
    - option_label (QLabel): Label widget for displaying "Wybierz sposób dodania sudoku:".
    - option_combo_box (QComboBox): Combo box widget for selecting the method of adding Sudoku puzzles.
    - go_back_button (QPushButton): Button widget for navigating back or canceling the operation.
    - add_button (QPushButton): Button widget for confirming and adding the Sudoku puzzle.

    Methods:
    - __init__(): Initializes the AddSudokuGUI with option label, combo box, buttons, and layout.
    """

    def __init__(self):
        """
        Initializes the AddSudokuGUI with necessary widgets and layout.
        """
        super().__init__()

        self.setWindowTitle("Dodaj Sudoku")
        self.setGeometry(100, 100, 300, 150)

        # Widgets setup
        self.option_label = QLabel("Wybierz sposób dodania sudoku:")
        self.option_combo_box = QComboBox()
        self.option_combo_box.addItems(["Dodaj z pliku", "Stwórz własny", "Dodaj ze zdjecia"]) 

        self.go_back_button = QPushButton("Cofnij")
        self.go_back_button.setObjectName("go_back_button")

        self.add_button = QPushButton("Dodaj")
        self.add_button.setObjectName("add_button")

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.option_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.option_combo_box)

        layout_for_buttons = QHBoxLayout()
        layout_for_buttons.addWidget(self.go_back_button)
        layout_for_buttons.addWidget(self.add_button)
        layout_for_buttons.setContentsMargins(0, 12, 0, 0)

        layout.addLayout(layout_for_buttons)
        layout.setContentsMargins(20, 20, 20, 20)

        # Main widget setup
        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

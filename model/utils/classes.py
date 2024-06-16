from PySide6.QtGui import QValidator, QPixmap
from PySide6.QtWidgets import QLineEdit, QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import QTimer, Qt
import platform
import os

class NonZeroValidator(QValidator):
    """
    Custom validator for QLineEdit to ensure only non-zero integer inputs are accepted.

    Methods:
    - validate(input_str, pos): Validates the input string and position.
    """

    def validate(self, input_str, pos):
        """
        Validate the input string to ensure it is a non-zero integer.

        Args:
        - input_str (str): Input string to be validated.
        - pos (int): Position of the cursor.

        Returns:
        - Tuple[QValidator.State, str, int]: Validation result with state, input string, and cursor position.
        """
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

class SolvedCell(QLineEdit):
    """
    Custom QLineEdit widget for displaying solved Sudoku puzzle cells.

    Methods:
    - copy_properties(other): Copies properties from another widget.
    """

    def __init__(self):
        """
        Initialize the SolvedCell widget.
        """
        super().__init__()
        self.setStyleSheet('color: #4e7;')
        self.setReadOnly(True)

    def copy_properties(self, other):
        """
        Copy properties from another widget to this widget.

        Args:
        - other (QLineEdit): Widget from which properties are copied.
        """
        self.setObjectName(other.objectName())
        self.setAlignment(other.alignment())
        self.setFixedSize(other.size())
        self.setValidator(other.validator())
        self.setMaxLength(other.maxLength())
        self.setText(other.text())

class ComputerCell(QLineEdit):
    """
    Custom QLineEdit widget for displaying computer-generated Sudoku puzzle cells.

    Methods:
    - copy_properties(other): Copies properties from another widget.
    """

    def __init__(self):
        """
        Initialize the ComputerCell widget.
        """
        super().__init__()
        self.setStyleSheet('color: #ddd;')
        self.setReadOnly(True)

    def copy_properties(self, other):
        """
        Copy properties from another widget to this widget.

        Args:
        - other (QLineEdit): Widget from which properties are copied.
        """
        self.setObjectName(other.objectName())
        self.setAlignment(other.alignment())
        self.setFixedSize(other.size())
        self.setValidator(other.validator())
        self.setMaxLength(other.maxLength())

class BlankCell(QLineEdit):
    """
    Custom QLineEdit widget for displaying blank Sudoku puzzle cells.

    Args:
    - color (str): Color of the text (default: 'white').

    Methods:
    - copy_properties(other): Copies properties from another widget.
    """

    def __init__(self, color='white'):
        """
        Initialize the BlankCell widget.

        Args:
        - color (str): Color of the text (default: 'white').
        """
        super().__init__()
        self.setStyleSheet(f'color: {color};')
        if platform.system() == 'Linux':
            self.setStyleSheet(f'color: black;')

    def copy_properties(self, other):
        """
        Copy properties from another widget to this widget.

        Args:
        - other (QLineEdit): Widget from which properties are copied.
        """
        self.setObjectName(other.objectName())
        self.setAlignment(other.alignment())
        self.setFixedSize(other.size())
        self.setValidator(other.validator())
        self.setMaxLength(other.maxLength())

class Stoper(QWidget):
    """
    Custom QWidget for a stopwatch timer.

    Methods:
    - initUI(): Initializes the user interface layout.
    - start_timer(): Starts the timer.
    - update_time(): Updates the displayed time.
    - get_time(): Retrieves the current time string.
    - set_time(time): Sets the time display to a specific string.
    - _time_to_seconds(time_str): Converts a time string to total seconds.
    """

    def __init__(self):
        """
        Initialize the Stoper widget.
        """
        super().__init__()
        self.initUI()

    def initUI(self):
        """
        Initialize the user interface layout for the Stoper widget.
        """
        layout = QHBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        stoper_icon_label = QLabel()
        start_icon_path = os.path.abspath(os.path.join("constants", "resources", "stopwatch.png"))
        stoper_icon = QPixmap(start_icon_path).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        stoper_icon_label.setPixmap(stoper_icon)
        stoper_icon_label.setAlignment(Qt.AlignRight)
        stoper_icon_label.setContentsMargins(0, 0, 0, 0)

        self.time_label = QLabel("00:00:00", self)
        self.time_label.setObjectName("time_label")
        self.time_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.time_label.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(stoper_icon_label)
        layout.addWidget(self.time_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        self.elapsed_time = 0

    def start_timer(self):
        """
        Starts the stopwatch timer.
        """
        self.timer.start(1000)

    def update_time(self):
        """
        Updates the displayed time by incrementing the elapsed time.
        """
        self.elapsed_time += 1
        hours, remainder = divmod(self.elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.time_label.setText(f"{hours:02}:{minutes:02}:{seconds:02}")

    def get_time(self):
        """
        Retrieves the current time displayed on the stopwatch.

        Returns:
        - str: Current time string in format "HH:MM:SS".
        """
        return self.time_label.text()

    def set_time(self, time):
        """
        Sets the time display to a specific string and starts the timer.

        Args:
        - time (str): Time string in format "HH:MM:SS".
        """
        self.time_label.setText(time)
        self.elapsed_time = self._time_to_seconds(time)
        self.start_timer()

    def _time_to_seconds(self, time_str):
        """
        Converts a time string in format "HH:MM:SS" to total seconds.

        Args:
        - time_str (str): Time string in format "HH:MM:SS".

        Returns:
        - int: Total seconds equivalent of the time string.
        """
        if time_str != "00:00:00" and time_str != "0":
            hours, minutes, seconds = map(int, time_str.split(':'))
        else:
            hours, minutes, seconds = 0, 0, 0

        return hours * 3600 + minutes * 60 + seconds

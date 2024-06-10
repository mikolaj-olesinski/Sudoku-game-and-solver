from PySide6.QtGui import QValidator, QPixmap
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PySide6.QtCore import QTimer, Qt
import os



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
        
class SolvedCell(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('color: #4e7;')
        self.setReadOnly(True)

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
        self.setStyleSheet('color: blue;')
        #self.setCursor(Qt.ArrowCursor)

    def copy_properties(self, other):
        self.setObjectName(other.objectName())
        self.setAlignment(other.alignment())
        self.setFixedSize(other.size())
        self.setValidator(other.validator())
        self.setMaxLength(other.maxLength())

class Stoper(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.setSpacing(5) 
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        stoper_icon_label = QLabel()
        start_incon_path = os.path.abspath(os.path.join("constants", "resources", "stopwatch.png"))
        stoper_icon = QPixmap(start_incon_path).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
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
        self.timer.start(1000) 

    def update_time(self):
        self.elapsed_time += 1
        hours, remainder = divmod(self.elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.time_label.setText(f"{hours:02}:{minutes:02}:{seconds:02}")

    def get_time(self):
        return self.time_label.text()

    def set_time(self, time):
        self.time_label.setText(time)
        self.elapsed_time = self._time_to_seconds(time)
        self.start_timer()

    def _time_to_seconds(self, time_str):
        hours, minutes, seconds = map(int, time_str.split(':'))
        return hours * 3600 + minutes * 60 + seconds
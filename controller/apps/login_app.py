from PySide6.QtWidgets import QApplication, QMainWindow
from view.login_gui import LoginWindow
from controller.controls.login_control import login_user

class login_app(LoginWindow):
    def __init__(self):
        super().__init__()
        self.cams = None
        self.show()
        self.login_button.clicked.connect(lambda: login_user(self))
        self.username_input.returnPressed.connect(lambda: login_user(self))

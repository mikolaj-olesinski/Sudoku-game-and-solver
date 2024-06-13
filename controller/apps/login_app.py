from PySide6.QtWidgets import QApplication, QMainWindow
from view.login_gui import LoginWindow
from controller.controls.login_control import login_user

class login_app(LoginWindow):

    '''
    The login_app class inherits from LoginWindow and provides the main 
    application logic for the login functionality.

    Methods
    -------
    __init__():
        Initializes the login window and connects signals to slots.
    """
    '''
    def __init__(self):
        '''
        Initializes the login_app instance. This method sets up the 
        login window and connects the login button and username input 
        to the login_user function.
        
        '''
        super().__init__()
        self.cams = None
        self.show()
        self.login_button.clicked.connect(lambda: login_user(self))
        self.username_input.returnPressed.connect(lambda: login_user(self))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import User_model
from database.addData import addUser
from PySide6.QtWidgets import QMessageBox
from controller.apps.sudoku_picker_app import sudoku_picker_app
from model.utils.func import check_username

def login_user(login_window):
    """
    Logs in a user based on the input username.

    This function interacts with the SQLite database to check if the user exists. If the user does not exist,
    it creates a new user entry. It then initializes the Sudoku picker application for the user.

    Parameters
    ----------
    login_window : LoginWindow
        The login window instance containing username input and handling UI interaction.

    Raises
    ------
    QMessageBox.warning
        If the username contains invalid characters or has an inappropriate length.
    """
    db_name = 'sudoku_database'
    engine = create_engine(f'sqlite:///database/{db_name}.sqlite3')

    Session = sessionmaker(bind=engine)
    session = Session()

    username = login_window.username_input.text()

    # Check if username is valid
    if not check_username(username):
        QMessageBox.warning(login_window, "Błąd", "Nazwa użytkownika zawiera niedozwolone znaki lub nieodpowiednią długość. Spróbuj ponownie.")
        login_window.username_input.clear()
    else:
        # Check if the user already exists in the database
        if session.query(User_model).filter_by(name=username).first():
            pass
        else:
            # If the user does not exist, add them to the database
            QMessageBox.information(login_window, "Informacja", f"Utworzono nowego użytkownika: {username}.")
            addUser(username)

        # Retrieve the user's ID
        user_id = session.query(User_model).filter_by(name=username).first().id

        session.close()
        print(f"User {username}, {user_id} logged in")

        # Initialize and show the Sudoku picker application for the user
        login_window.cams = sudoku_picker_app(user_id, login_window)
        login_window.cams.show()
        login_window.cams.setWindowTitle(f"Użytkownik: {username}")
        login_window.close()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import User_model
from PySide6.QtWidgets import QMessageBox
from datetime import datetime
from controller.apps.sudoku_app import sudoku_app

def login_user(login_window):
    db_name = 'sudoku_database'
    engine = create_engine(f'sqlite:///database/{db_name}.sqlite3')

    Session = sessionmaker(bind=engine)
    session = Session()

    username = login_window.username_input.text()

    if session.query(User_model).filter_by(name=username).first():
        QMessageBox.information(login_window, "Informacja", f"Zalogowano jako {username}")
    else:
        new_user = User_model(name=username, created_at=datetime.now())
        session.add(new_user)
        session.commit()
        QMessageBox.information(login_window, "Informacja", f"Utworzono użytkownika {username}")

    session.close()
    login_window.cams = sudoku_app()
    login_window.cams.show()
    login_window.close()


import sys
import os
from sqlalchemy import create_engine
from models import Base

def create_database(db_name):
    engine = create_engine(f'sqlite:///{db_name}.sqlite3')
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Zła liczba argumentów, podaj nazwę bazy danych, np. 'python create_database.py baza_danych'")
        sys.exit(1)
    
    db_name = sys.argv[1]
    db_path = f'{db_name}.sqlite3'
    
    if os.path.exists(db_path):
        print(f"Baza danych '{db_path}' już istnieje.")
    else:
        create_database(db_name)
        print(f"Baza danych '{db_path}' została utworzona pomyślnie.")

import sys
import os
from sqlalchemy import create_engine
from database.models import Base

def create_database(db_name):

    database_path = f'database/{db_name}.sqlite3'

    if os.path.exists(database_path):
        pass
    else:
        engine = create_engine(f'sqlite:///{database_path}')
        Base.metadata.create_all(engine)
        print(f'Database {db_name} created')

if __name__ == '__main__':
    db_name = 'sudoku_database'
    create_database(db_name)
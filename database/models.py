from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Sudoku_model(Base):
    __tablename__ = 'sudoku'
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    data = Column(String)
    solved_data = Column(String)
    difficulty = Column(String)



class User_model(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime)


class UsersSudoku_model(Base):
    __tablename__ = 'users_sudoku'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    sudoku_id = Column(Integer, ForeignKey('sudoku.id'), primary_key=True)
    started_at = Column(DateTime)
    last_saved = Column(DateTime)
    time = Column(Integer)
    is_solved = Column(Boolean)
    current_sudoku_state = Column(String)
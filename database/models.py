from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Sudoku_model(Base):
    __tablename__ = 'sudoku'
    id = Column(Integer, primary_key=True)
    data = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    solved = Column(String)


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
    finished_at = Column(DateTime)
    time = Column(Integer)
    cuurent_sudoku_state = Column(String)

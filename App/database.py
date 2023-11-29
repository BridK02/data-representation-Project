from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base

db = SQLAlchemy()

# database.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Classes(Base):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250))
    instructor = Column(String(250))
    fee = Column(Integer)

    # Correct the relationship definition
    bookings = relationship('Bookings', back_populates='yoga_class')

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    email = Column(String(250), unique=True)
    dob = Column(Date) 
    password = Column(String(250))
    bookings = relationship('Bookings', back_populates='user')

class Bookings(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', back_populates='bookings')
    class_id = Column(Integer, ForeignKey('classes.id'))
    yoga_class = relationship('Classes', back_populates='bookings')



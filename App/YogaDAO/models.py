from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Classes(db.Model):
    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(250))
    instructor = Column(String(250))
    fee = Column(Integer)
    bookings = relationship('Bookings', back_populates='yoga_class')

class Users(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    email = Column(String(250), unique=True)
    dob = Column(Date) 
    password = Column(String(250))  # Add the password column
    bookings = relationship('Bookings', back_populates='user')

class Bookings(db.Model):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('Users', back_populates='bookings')
    class_id = Column(Integer, ForeignKey('classes.id'))
    yoga_class_ = relationship('Classes', back_populates='bookings')








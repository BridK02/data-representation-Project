from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt
from . import db 


bcrypt = Bcrypt()

class Classes(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    instructor = db.Column(db.String(255), nullable=False)
    fee = db.Column(db.Integer, nullable=False)
    image_filename = db.Column(db.String(255), nullable=False, default="default.jpg")
    bookings = relationship('Bookings', back_populates='yoga_class')

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250))
    email = Column(String(250), unique=True)
    dob = Column(Date)
    password = Column(String(250))
    bookings = relationship('Bookings', back_populates='user')

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def is_active(self):
        # You can add additional logic here if needed
        return True

class Bookings(db.Model):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='bookings')
    class_id = Column(Integer, ForeignKey('classes.id'))
    yoga_class = relationship('Classes', back_populates='bookings')

from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from flask_bcrypt import Bcrypt
from .base import Base

from . import db 


bcrypt = Bcrypt()

class Classes(db.Model):
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    instructor = db.Column(db.String(255), nullable=False)
    fee = db.Column(db.Integer, nullable=False)
    image_filename = db.Column(db.String(255), nullable=False, default="default.jpg")
    bookings = db.relationship('Bookings', back_populates='yoga_class', primaryjoin="Classes.id == Bookings.class_id")


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250))
    email = db.Column(db.String(250), unique=True)
    dob = db.Column(db.Date)
    password = db.Column(String(250))
    bookings = db.relationship('Bookings', back_populates='user')

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def is_active(self):
        return True

class user_classes(db.Model):
    __tablename__ = 'user_classes'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), primary_key=True)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)

class Bookings(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates='bookings')
    yoga_class = db.relationship('Classes', back_populates='bookings')
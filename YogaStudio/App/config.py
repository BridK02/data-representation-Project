# config.py
class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'Myterypassword'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/Yogastudio'
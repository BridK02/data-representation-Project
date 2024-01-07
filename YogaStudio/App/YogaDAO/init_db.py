import sys
sys.path.insert(0, '/home/G00411262/data-representation-Project/YogaStudio')
from . import db
from .models import User, Classes, Bookings

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
from . import db
from .models import User, Classes, Bookings

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
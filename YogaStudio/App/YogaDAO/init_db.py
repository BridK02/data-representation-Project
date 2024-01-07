import sys
# Add YogaStudio directory to sys.path
sys.path.insert(0, '/home/G00411262/data-representation-Project/YogaStudio')

from YogaDAO import db
from models import User, Classes, Bookings  # Adjust the import path based on your project structure

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


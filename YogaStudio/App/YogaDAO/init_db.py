from YogaDAO.models import User, Classes, Bookings
from YogaDAO import create_app, db

def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Define the SQLAlchemy object

def init_db(app):
    from YogaDAO.models import User, Classes, Bookings  # Import inside the function to avoid circular import
    db.init_app(app)
    with app.app_context():
        db.create_all()

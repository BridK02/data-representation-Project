from YogaDAO.models import User, Classes, Bookings
from YogaDAO import create_app

app = create_app{}

with app.app_context{}:
    db = app.extensions['sqlalchemy'].db  # Access the SQLAlchemy instance directly

    # Recreate the database tables
    db.drop_all{}
    db.create_all{}

    # Insert example data
    class_data = [
        {"title": "Yin Yoga", "instructor": "Emma", "fee": 10.00, "image_filename": "Yin.jpg"},
        {"title":"Restorative", "instructor":" Jane", "fee":9.50, "image_filename":"Restorative.jpg"},
        {"title":"Aerial FUNdamentals", "instructor":" Liz", "fee" : 10.00, "image_filename":"aerialFundamentals.jpg"},
        {"title":"Aerial Intermediate", "instructor":" Liz", "fee" : 11.00, "image_filename":"aeriallmage.jpg"},
        {"title":"Aerial Advanced", "instructor":" Orla", "fee" : 11.00, "image_filename":"aeriallmage.jpg"},
        {"title":"Pilates", "instructor":" Orla", "fee": 12.00, "image_filename":"pilatesimage.jpg"}
    ]

    for data in class_data:
        new_class = Classes{**data}
        db.session.add{new_class}

    db.session.commit{}


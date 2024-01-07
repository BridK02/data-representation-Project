import sys
import secrets
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy import create_engine
from YogaStudio.App.YogaDAO.dbconfigpa import mysql
from .YogaDAO import db
from .YogaDAO import init_db
#from YogaStudio.App.config import Config
from YogaStudio.App.create_app import create_app

app = create_app()

app = Flask(__name__, static_url_path='/static', template_folder='templates')
 

app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{mysql['user']}:{mysql['password']}@{mysql['host']}/{mysql['database']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
secret_key = app.config['SECRET_KEY']

init_db(app) 

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):  # Function to load user from the database
    return db.session.query(User).get(int(user_id))

# Define routes and views
@app.route('/')
def home():
    classes = Classes.query.all()  # Query all available classes

    profile_link = url_for('profile')
    booking_summary_link = url_for('booking_summary', class_id=1)

    return render_template('index.html', classes=classes, profile_link=profile_link, booking_summary_link=booking_summary_link)
@app.route('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate the form data (add more validation as needed)
        if not name or not email or not password:
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('register'))

        # Check if the email is already registered
        existing_user = db.session.query(User).filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', 'error')
            return redirect(url_for('register'))

        # Create a new user instance
        new_user = User(name=name, email=email)
        new_user.set_password(password)

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        session['registered'] = True
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the user exists and entered the correct password
        user = db.session.query(User).filter_by(email=email).first()

        if user and user.check_password(password):
            # User exists and password is correct
            login_user(user)

            # Set session variable to indicate successful login
            session['logged_in'] = True

            return redirect(url_for('home'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')

@app.route('/profile')
@login_required  # Use a decorator to ensure the user is logged in
def profile():
    # You can directly use current_user from Flask-Login
    user = current_user
    return render_template('profile.html', user=user)


@app.route('/booking_summary/<int:class_id>')
@login_required
def booking_summary(class_id=None):
    print(f"Received class ID in booking_summary: {class_id}")
    # Retrieve the selected class
    yoga_class = Classes.query.get(class_id)

    # Ensure the class exists
    if not yoga_class:
        flash('Selected class not found', 'error')
        return redirect(url_for('home'))

    # Get all booked classes for the current user
    booked_classes = current_user.bookings

     # Calculate total cost based on all booked classes
    total_cost = sum(booked_class.yoga_class.fee for booked_class in booked_classes)
    try:
        # Commit changes to the database
        db.session.commit()
    except Exception as e:
        # Handle the exception, print an error message, and rollback changes
        print(f"Error during commit: {e}")
        db.session.rollback()

    # Render the booking summary template with relevant data
    return render_template('booking_summary.html', booked_classes=booked_classes, total_cost=total_cost)

@app.route('/bookings', methods=['GET', 'POST'])
@login_required
def bookings():
    user_selected_class_id = None

    if request.method == 'POST':
        user_name = request.form.get('name')
        user_email = request.form.get('email')
        user_selected_class_title = request.form.get('class_title')

        user_selected_class = Classes.query.filter_by(title=user_selected_class_title).first()

        if user_selected_class:
            user_selected_class_id = user_selected_class.id
            print(f"Selected class ID: {user_selected_class_id}")

            # Create a new booking and add it to the database
            new_booking = Bookings(class_id=user_selected_class_id, user_id=current_user.id)
            db.session.add(new_booking)
            db.session.commit()

            return redirect(url_for('booking_summary', class_id=user_selected_class_id))
        else:
            flash('Invalid class title selected.')
            return redirect(url_for('bookings'))

    classes = Classes.query.all()
    return render_template('bookings.html', classes=classes)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

def recreate_database(database):
    database.drop_all()
    database.create_all()


def insert_example_data(database):
    class_data = [
        {"title": "Yin Yoga", "instructor": "Emma", "fee": 10.00, "image_filename": "Yin.jpg"},
        {"title": "Restorative Yoga", "instructor": "Jane", "fee": 9.50, "image_filename": "Restorative.jpg"},
        {"title": "Aerial FUNdamentals", "instructor": "Liz", "fee": 11.00, "image_filename": "aerialFundamentals.jpg"},
        {"title": "Aerial Intermediate", "instructor": "Liz", "fee": 11.00, "image_filename": "aerialImage.jpg"},
        {"title": "Aerial Advanced", "instructor": "Orla", "fee": 11.00, "image_filename": "aerialImage.jpg"},
        {"title": "Pilates", "instructor": "Orla", "fee": 12.00, "image_filename": "pilatesImage.jpg"},
    ]

    for data in class_data:
        new_class = Classes(**data)
        db.session.add(new_class)

    database.session.commit()

if __name__ == '__main__':
    

    app.run(debug=False)


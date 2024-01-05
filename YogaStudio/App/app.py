import sys
import secrets
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from YogaDAO import db
from YogaDAO.models import User, Classes, Bookings
from config import SECRET_KEY

app = Flask(__name__, static_url_path='/static', template_folder='templates')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/Yogastudio'
app.config['SECRET_KEY'] = SECRET_KEY


migrate = Migrate(app, db)
bcrypt = Bcrypt(app)  # Use bcrypt from Flask-Bcrypt
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):  # Function to load user from the database
    return db.session.query(User).get(int(user_id))

# Define routes and views
@app.route('/')
def home():
    return render_template('index.html')

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

@app.route('/bookings', methods=['GET', 'POST'])
@login_required
def bookings():
    if request.method == 'POST':
        class_selected = request.form.get('class')
        user_name = request.form.get('name')
        user_email = request.form.get('email')

        # Validate the form data (add more validation as needed)
        if not class_selected or not user_name or not user_email:
            flash('Invalid form data. Please fill in all fields.', 'error')
            return redirect(url_for('bookings'))

        # Query the database to find the selected class
        selected_class = Classes.query.filter_by(id=class_selected).first()

        if not selected_class:
            flash('Invalid class selection. Please try again.', 'error')
            return redirect(url_for('bookings'))

        # Create a new booking instance
        new_booking = Bookings(user=current_user, yoga_class=selected_class)
        # Add additional logic to save other booking details if needed

        # Add the new booking to the database
        db.session.add(new_booking)
        db.session.commit()

        flash('Booking successful!', 'success')
        return redirect(url_for('home'))
    # For GET requests, render the bookings page
    classes = Classes.query.all()  # Query all available classes

    # Check if the user has completed registration and login
    if 'registered' not in session or 'logged_in' not in session:
        flash('You need to register and log in before booking a class.', 'info')
        return redirect(url_for('register'))

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
        {"title": "Yin Yoga", "instructor": "Emma", "fee": 1000, "image_filename": "Yin.jpg"},
        {"title": "Restorative Yoga", "instructor": "Jane", "fee": 950, "image_filename": "Restorative.jpg"},
        {"title": "Aerial FUNdamentals", "instructor": "Liz", "fee": 1100, "image_filename": "aerialFundamentals.jpg"},
        {"title": "Aerial Intermediate", "instructor": "Liz", "fee": 1100, "image_filename": "aeriallmage.jpg"},
        {"title": "Aerial Advanced", "instructor": "Orla", "fee": 1100, "image_filename": "aeriallmage.jpg"},
        {"title": "Pilates", "instructor": "Orla", "fee": 1200, "image_filename": "pilatesimage.jpg"},
    ]

    for data in class_data:
        new_class = Classes(**data)
        db.session.add(new_class)

    database.session.commit()
    

if __name__ == '__main__':
    with app.app_context():
        db.init_app(app)
        recreate_database(db)  # Pass the db instance as an argument
        insert_example_data(db)

    app.run(debug=True)
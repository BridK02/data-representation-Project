import sys
import secrets
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_migrate import Migrate
from YogaDAO import db
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from YogaDAO.models import User, Classes, Bookings
from config import SECRET_KEY 

app = Flask(__name__, static_url_path='/static', template_folder='templates')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/Yogastudio'
app.config['SECRET_KEY'] = SECRET_KEY  

db.init_app(app)

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)  
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
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
        existing_user = User.query.filter_by(email=email).first()
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
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
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
    return render_template('bookings.html', classes=classes)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
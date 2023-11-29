import sys
import secrets
from flask import Flask, jsonify, request, abort, render_template, flash
from database import db
from YogaDAO.models import Classes, Users, Bookings
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate 


engine = create_engine('mysql://root:root@localhost/Yogastudio', echo=True)

Session = sessionmaker(bind=engine)
session= Session()

app = Flask(__name__, static_url_path='', static_folder='.', template_folder='templates')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/Yogastudio'
app.config['SECRET_KEY'] = secrets.token_hex(16)  

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)  
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250))
    email = db.Column(db.String(250), unique=True)
    dob = db.Column(db.Date)
    password = db.Column(db.String(250))

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
# Define routes and views
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # ... (your existing registration logic)

        # Use set_password to hash and set the password
        new_user.set_password(password)
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

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database tables
with app.app_context():
    db.create_all()




@app.route('/profile')
@login_required
def profile():
    return f'Hello, {current_user.name}!'

@app.route('/bookings', methods=['GET', 'POST'])
@login_required
def bookings():
    if request.method == 'POST':
        # Handle form data submitted via POST
        class_selected = request.form.get('class')
        user_name = request.form.get('name')
        user_email = request.form.get('email')

        # Example: Check if the form data is valid and store it in the database
        if class_selected and user_name and user_email:
            # Add your logic to save the booking data to the database
            flash('Booking successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid form data. Please fill in all fields.', 'error')

    # Render the bookings page for GET requests
    return render_template('bookings.html')





@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))






if __name__ == '__main__':
    app.run(debug=True)



'''#curl "http://127.0.0.1:5000/books"
@app.route('/books')
def getAll():
    return jsonify(books)

#curl "http://127.0.0.1:5000/books/2"
@app.route('/books/<int:id>')
def findById(id):
    foundBooks = list(filter(lambda t: t['id'] == id, books))
    if len(foundBooks) == 0:
        return jsonify ({}) , 204

    return jsonify(foundBooks[0])

#curl  -i -H "Content-Type:application/json" -X POST -d "{\"Title\":\"hello\",\"Instructor\":\"someone\",\"Price\":123}" http://127.0.0.1:5000/books
@app.route('/books', methods=['POST'])
def create():
    global nextId
    if not request.json:
        abort(400)
    # other checking 
    book = {
        "id": nextId,
        "Title": request.json['Title'],
     "Instructor": request.json['Instructor'],
        "Price": request.json['Price'],
    }
    nextId += 1
    books.append(book)
    return jsonify(book)

#curl  -i -H "Content-Type:application/json" -X PUT -d "{\"Title\":\"hello\",\"Instructor\":\"someone\",\"Price\":123}" http://127.0.0.1:5000/books/1
@app.route('/books/<int:id>', methods=['PUT'])
def update(id):
    foundBooks = list(filter(lambda t: t['id']== id, books))
    if (len(foundBooks) == 0):
        abort(404)
    foundBook = foundBooks[0]
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'Price' in reqJson and type(reqJson['Price']) is not int:
        abort(400)

    if 'Title' in reqJson:
        foundBook['Title'] = reqJson['Title']
    if 'Instructor' in reqJson:
        foundBook['Instructor'] = reqJson['Instructor']
    if 'Price' in reqJson:
        foundBook['Price'] = reqJson['Price']
    
    return jsonify(foundBook)
        

    return "in update for id "+str(id)

@app.route('/books/<int:id>' , methods=['DELETE'])
def delete(id):
    foundBooks = list(filter(lambda t: t['id']== id, books))
    if (len(foundBooks) == 0):
        abort(404)
    books.remove(foundBooks[0])
    return jsonify({"done":True})

yoga titles=[
    { "id":1, "Title":"Yin", "Instructor":"Emma", "Price":1000},
    { "id":2, "Title":"Restortative", "Instructor":"Jane", "Price":950},
    { "id":3, "Title":"Aerial FUNdamentals", "Instructor":" Liz", "Price":1100}
    { "id":4 "Title":"Aerial Intermediate", "Instructor":" Liz", "Price":1100}
    { "id":4 "Title":"Aerial Advanced", "Instructor":" Orla", "Price":1100}
    { "id":5 "Title":"Pilates", "Instructor":" Orla", "Price":1200}
]




if __name__ == '__main__' :
    app.run(debug= True)'''
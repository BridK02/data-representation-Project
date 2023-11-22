from flask import Flask, jsonify, request, abort, render_template
from database.models import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://username:password@localhost/Yogastudio', echo=True)

Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__, static_url_path='', static_folder='.')

'''yoga titles=[
    { "id":1, "Title":"Yin", "Instructor":"Emma", "Price":1000},
    { "id":2, "Title":"Restortative", "Instructor":"Jane", "Price":950},
    { "id":3, "Title":"Aerial FUNdamentals", "Instructor":" Liz", "Price":1100}
    { "id":4 "Title":"Aerial Intermediate", "Instructor":" Liz", "Price":1100}
    { "id":4 "Title":"Aerial Advanced", "Instructor":" Orla", "Price":1100}
    { "id":5 "Title":"Pilates", "Instructor":" Orla", "Price":1200}
]
nextId=6
#app = Flask(__name__)

#@app.route('/')
#def index():
#    return "Hello, World!"'''


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/database_name'
db.init_app(app)

# Create database tables
with app.app_context():
    db.create_all()

# Define routes and views
@app.route('/')
def home():
    return render_template('index.html')

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



if __name__ == '__main__' :
    app.run(debug= True)'''
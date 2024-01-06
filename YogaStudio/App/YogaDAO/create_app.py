from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_url_path='/static', template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)

    return app

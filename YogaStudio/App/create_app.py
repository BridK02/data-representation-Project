from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from YogaStudio.App.config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__, static_url_path='/static', template_folder='templates')
    app.config.from_object(config_class)

    db.init_app(app)  # Initialize SQLAlchemy with the app

    # Other configurations and extensions

    return app


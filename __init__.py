from flask import Flask

# Create the Flask application instance
app = Flask(__name__)

# Import and register blueprints or other components here
from . import create_app  # Assuming create_app is defined in YogaDAO
app = create_app(app)


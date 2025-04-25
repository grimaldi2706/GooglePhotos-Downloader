from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    # Load the configuration from the Config class
    app.config.from_object(Config)

    from .routes import main
    app.register_blueprint(main)

    return app

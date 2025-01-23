from flask import Flask
from config import Config
from app.database import MongoDatabase

mongo = MongoDatabase()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize MongoDB
    mongo.init_app(app)

    # Register blueprints
    from app.routes import main

    app.register_blueprint(main)

    return app

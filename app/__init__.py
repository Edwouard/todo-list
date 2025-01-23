from flask import Flask
from config import Config
def create_app(config_class=Config):
    app = Flask(_name_)  
    app.config.from_object(config_class)
    return app
from flask import Flask
from config import Config
from app.database import MongoDatabase

mongo = MongoDatabase()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialisation de MongoDB
    mongo.init_app(app)

    # Enregistrement des blueprints
    from app.routes import main

    app.register_blueprint(main)

    if __name__ == "__main__":
        # Configuration du serveur pour le développement
        app.run(
            host=app.config.get("HOST", "0.0.0.0"),
            port=app.config.get("PORT", 5000),
            debug=app.config.get("DEBUG", True),
        )

    return app

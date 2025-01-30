from flask import Flask
from config import Config
from app.database import MongoDatabase
import logging

mongo = MongoDatabase()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)


    logger.info("Initialisation de l'application Flask")

    try:
        # Initialisation de MongoDB
        logger.info(
            f"Tentative de connexion à MongoDB sur {app.config['MONGO_HOST']}:{app.config['MONGO_PORT']}"
        )
        mongo.init_app(app)
        logger.info("Connexion MongoDB établie avec succès")
    except Exception as e:
        logger.error(f"Erreur de connexion à MongoDB: {e}")
        raise

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

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Configuration serveur Flask
    HOST = os.environ.get("FLASK_RUN_HOST", "0.0.0.0")
    PORT = int(os.environ.get("FLASK_RUN_PORT", 5000))
    DEBUG = os.environ.get("FLASK_ENV") == "development"

    # Configuration MongoDB
    MONGO_HOST = os.environ.get("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.environ.get("MONGO_PORT", 27017))
    MONGO_USER = os.environ.get("MONGO_USER", "todo_user")
    MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD", "passer")
    MONGO_DB = os.environ.get("MONGO_DB", "todo_db")

    MONGO_URI = os.environ.get(
        "MONGO_URI",
        f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}?authSource=todo_db",
    )

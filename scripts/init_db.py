from pymongo import MongoClient
from pymongo.errors import OperationFailure


def init_mongodb():
    """
    Initialise MongoDB sans authentification, puis crée un utilisateur admin et un utilisateur pour l'application.
    """
    try:
        # Connexion sans authentification avec l'utilisateur admin
        client = MongoClient("mongodb://localhost:27017/")

        # Vérification que MongoDB est démarré
        client.admin.command("ping")
        print("✓ Connexion à MongoDB établie (sans authentification)")

        # Création de la base de données et de l'utilisateur pour l'application
        db = client.todo_db
        db.command(
            "createUser",
            "todo_user",
            pwd="passer",
            roles=[
                {"role": "readWrite", "db": "todo_db"},
                {"role": "dbAdmin", "db": "todo_db"},
            ],
        )
        print("✓ Utilisateur de l'application créé")

    except OperationFailure as e:
        if "already exists" in str(e):
            print("L'utilisateur existe déjà")
        else:
            print(f"Erreur lors de la création : {e}")
            return False


init_mongodb()

from pymongo import MongoClient


def init_mongodb():
    """
    Initialise MongoDB sans authentification, puis crée un utilisateur admin et un utilisateur pour l'application.
    """
    try:
        # Connexion sans authentification
        client = MongoClient("mongodb://localhost:27017/")

        # Vérification que MongoDB est démarré
        client.admin.command("ping")
        print("✓ Connexion à MongoDB établie (sans authentification)")


        # Connexion avec l'utilisateur admin 
        admin_client = MongoClient(
            "mongodb://localhost:27017/admin"
        )

        # Création de la base de données et de l'utilisateur pour l'application
        db = admin_client.todo_db
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

    except Exception as e:
        if "already exists" not in str(e):
                        print(f"Erreur lors de la gestion des utilisateurs : {str(e)}")
                        return False


init_mongodb()

from flask import current_app
from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from bson.objectid import ObjectId
import logging
import time


class MongoDatabase:
    def __init__(self, app=None):
        self.client = None
        self.db = None
        if app is not None:
            self.init_app(app)


    def init_app(self, app):
        retry_count = 3
        while retry_count > 0:
            try:
                self.client = MongoClient(app.config["MONGO_URI"])
                # Test la connexion
                self.client.admin.command("ping")
                self.db = self.client.get_database("todo_db")
                app.db = self.db
                logging.info("MongoDB connecté avec succès")
                return
            except Exception as e:
                retry_count -= 1
                if retry_count == 0:
                    logging.error(f"Échec de connexion MongoDB après 3 tentatives: {e}")
                    raise
                logging.warning(f"Tentative de reconnexion ({3-retry_count}/3)")
                time.sleep(2)

    def _ensure_indexes(self):
        """Création des index nécessaires"""
        try:
            # Index pour la recherche textuelle
            self.db.todo.create_index([("name", "text"), ("desc", "text")])
            # Index pour le tri par date
            self.db.todo.create_index([("date", ASCENDING)])
            logging.info("Index MongoDB créés avec succès")
        except Exception as e:
            logging.error(f"Erreur lors de la création des index: {e}")

    def get_todos(self, filter_dict=None, sort_by=None):
        """Récupère les tâches avec filtre et tri optionnels"""
        try:
            cursor = self.db.todo.find(filter_dict or {})
            if sort_by:
                cursor = cursor.sort(sort_by)
            return list(cursor)
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des tâches: {e}")
            return []

    def add_todo(self, todo_data):
        """Ajoute une nouvelle tâche"""
        try:
            result = self.db.todo.insert_one(todo_data)
            return result.inserted_id
        except Exception as e:
            logging.error(f"Erreur lors de l'ajout d'une tâche: {e}")
            return None

    def update_todo(self, todo_id, update_data):
        """Met à jour une tâche existante"""
        try:
            result = self.db.todo.update_one(
                {"_id": ObjectId(todo_id)}, {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            logging.error(f"Erreur lors de la mise à jour de la tâche: {e}")
            return False

    def delete_todo(self, todo_id):
        """Supprime une tâche"""
        try:
            result = self.db.todo.delete_one({"_id": ObjectId(todo_id)})
            return result.deleted_count > 0
        except Exception as e:
            logging.error(f"Erreur lors de la suppression de la tâche: {e}")
            return False

    def search_todos(self, query, limit=10):
        """Recherche dans les tâches"""
        try:
            return list(
                self.db.todo.find(
                    {"$text": {"$search": query}}, {"score": {"$meta": "textScore"}}
                )
                .sort([("score", {"$meta": "textScore"})])
                .limit(limit)
            )
        except Exception as e:
            logging.error(f"Erreur lors de la recherche: {e}")
            return []

    def get_stats(self):
        """Récupère les statistiques des tâches"""
        try:
            total = self.db.todo.count_documents({})
            completed = self.db.todo.count_documents({"done": "yes"})
            pending = self.db.todo.count_documents({"done": "no"})
            return {
                "total": total,
                "completed": completed,
                "pending": pending,
                "completion_rate": (completed / total * 100) if total > 0 else 0,
            }
        except Exception as e:
            logging.error(f"Erreur lors de la récupération des statistiques: {e}")
            return {"total": 0, "completed": 0, "pending": 0, "completion_rate": 0}

    def close(self):
        """Ferme la connexion à MongoDB"""
        if self.client:
            self.client.close()
            logging.info("Connexion MongoDB fermée")

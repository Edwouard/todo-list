from flask import current_app
from pymongo import MongoClient
from bson.objectid import ObjectId


class MongoDatabase:
    def __init__(self, app=None):
        self.client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.client = MongoClient(app.config["MONGO_URI"])
        self.db = self.client.get_default_database()

        # Add database to app context
        app.db = self.db

    def get_todos(self, filter_dict=None):
        return self.db.todo.find(filter_dict or {})

    def add_todo(self, todo_data):
        return self.db.todo.insert_one(todo_data)

    def update_todo(self, todo_id, update_data):
        return self.db.todo.update_one(
            {"_id": ObjectId(todo_id)}, {"$set": update_data}
        )

    def delete_todo(self, todo_id):
        return self.db.todo.delete_one({"_id": ObjectId(todo_id)})



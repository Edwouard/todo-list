import pytest
from app import create_app
from app.database import MongoDatabase


@pytest.fixture
def app():
    app = create_app("config.TestConfig")
    return app


def test_mongodb_connection(app):
    with app.app_context():
        assert app.db is not None


def test_add_todo(app):
    with app.app_context():
        todo = {
            "name": "Test Todo",
            "desc": "Test Description",
            "date": "2024-01-23",
            "pr": "High",
            "done": "no",
        }
        result = app.db.todo.insert_one(todo)
        assert result.inserted_id is not None

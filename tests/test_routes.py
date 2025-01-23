import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app('config.TestConfig')
    with app.test_client() as client:
        yield client

def test_home_page(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_add_todo(client):
    rv = client.post('/action', data={
        'name': 'Test Todo',
        'desc': 'Test Description',
        'date': '2024-01-23',
        'pr': 'High'
    })
    assert rv.status_code == 302
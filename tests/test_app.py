import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_todos_empty(client):
    rv = client.get('/todos')
    assert rv.status_code == 200
    assert rv.json == []

def test_add_todo(client):
    rv = client.post('/todos', json={'task': 'Test task'})
    assert rv.status_code == 201
    assert rv.json['task'] == 'Test task'
    assert rv.json['completed'] is False

def test_add_todo_invalid(client):
    rv = client.post('/todos', json={})
    assert rv.status_code == 400
    assert 'error' in rv.json

def test_update_todo(client):
    client.post('/todos', json={'task': 'Test task'})
    rv = client.put('/todos/1', json={'task': 'Updated task', 'completed': True})
    assert rv.status_code == 200
    assert rv.json['task'] == 'Updated task'
    assert rv.json['completed'] is True

def test_delete_todo(client):
    client.post('/todos', json={'task': 'Test task'})
    rv = client.delete('/todos/1')
    assert rv.status_code == 200
    assert rv.json['message'] == 'Todo deleted'

import pytest
from src.app import app
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client

def test_landing_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the Todo API' in response.data

def test_login_required():
    with app.test_client() as client:
        response = client.get('/dashboard')
        assert response.status_code == 401
        assert b'Authentication required' in response.data

def test_login_logout():
    with app.test_client() as client:
        # Test login
        response = client.post('/login', json={
            'username': os.getenv('ADMIN_USERNAME', 'admin'),
            'password': os.getenv('ADMIN_PASSWORD', 'password')
        })
        assert response.status_code == 200
        assert b'Login successful' in response.data

        # Test logout
        response = client.post('/logout')
        assert response.status_code == 200
        assert b'Logout successful' in response.data

def test_todo_operations():
    with app.test_client() as client:
        # Login first
        client.post('/login', json={
            'username': os.getenv('ADMIN_USERNAME', 'admin'),
            'password': os.getenv('ADMIN_PASSWORD', 'password')
        })

        # Create todo
        response = client.post('/todos', json={'title': 'Test Todo'})
        assert response.status_code == 201
        todo_id = response.json['id']

        # Get todos
        response = client.get('/todos')
        assert response.status_code == 200
        assert len(response.json) > 0

        # Update todo
        response = client.put(f'/todos/{todo_id}', json={'status': 'completed'})
        assert response.status_code == 200
        assert response.json['status'] == 'completed'

        # Delete todo
        response = client.delete(f'/todos/{todo_id}')
        assert response.status_code == 204 
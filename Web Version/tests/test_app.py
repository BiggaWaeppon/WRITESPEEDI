import pytest
from app import create_app, db
from models import User

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_app_exists(app):
    assert app is not None

def test_app_is_testing(app):
    assert app.config['TESTING'] is True

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'WriteSpeedi' in response.data

def test_register_page(client):
    response = client.post('/register', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert b'Registration successful' in response.data

def test_login_page(client):
    # First register a user
    client.post('/register', json={
        'username': 'testuser',
        'password': 'password123'
    })
    
    # Then try to login
    response = client.post('/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert b'Login successful' in response.data

def test_start_test_page(client):
    # First login a user
    client.post('/register', json={
        'username': 'testuser',
        'password': 'password123'
    })
    client.post('/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    
    # Then access start_test
    response = client.get('/start_test')
    assert response.status_code == 200
    assert b'Typing Test' in response.data

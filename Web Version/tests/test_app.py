import pytest
from writespeedi.app import create_app, db
from writespeedi.models import User

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
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_start_test_page(client):
    response = client.get('/start_test')
    assert response.status_code == 200
    assert b'Typing Test' in response.data

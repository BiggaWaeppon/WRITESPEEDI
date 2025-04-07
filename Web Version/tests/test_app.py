import pytest
from app import app, db
from models import User

def test_app_exists():
    assert app is not None

def test_app_is_testing():
    assert app.config['TESTING'] is True

def test_home_page():
    response = app.test_client().get('/')
    assert response.status_code == 200
    assert b'WriteSpeedi' in response.data

def test_register_page():
    response = app.test_client().get('/register')
    assert response.status_code == 200
    assert b'Register' in response.data

def test_login_page():
    response = app.test_client().get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_start_test_page():
    response = app.test_client().get('/start_test')
    assert response.status_code == 200
    assert b'Typing Test' in response.data

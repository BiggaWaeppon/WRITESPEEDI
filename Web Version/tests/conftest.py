import pytest
from app import create_app, db
from models import User

@pytest.fixture(scope='module')
def test_client():
    # Create a Flask app configured for testing
    flask_app = create_app('testing')
    
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!

@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()
    
    # Insert test data
    test_user = User(username='testuser', email='test@example.com')
    test_user.set_password('password123')
    db.session.add(test_user)
    
    # Commit the changes for the tests
    db.session.commit()
    
    yield db  # this is where the testing happens!
    
    # Drop the database table after the test
    db.session.remove()
    db.drop_all()

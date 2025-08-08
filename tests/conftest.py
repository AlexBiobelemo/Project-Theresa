import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def app():
    """Create and configure a new app instance for each test module."""
    # Create a test client using the Flask application configured for testing
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # Use an in-memory database
        "WTF_CSRF_ENABLED": False,  # Disable CSRF for testing forms
        "SERVER_NAME": "127.0.0.1" # Helps with url_for
    })

    with app.app_context():
        db.create_all() # Create all database tables

    yield app

    with app.app_context():
        db.drop_all() # Drop all database tables

@pytest.fixture(scope='module')
def client(app):
    """A test client for the app."""
    return app.test_client()

import pytest
from app import app as flask_app
from models import db as app_db
from Dummy_ERP.app import app as dummy_app, db as dummy_db


@pytest.fixture
def app():
    """Create and configure a clean Flask test application."""
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })
    with flask_app.app_context():
        app_db.create_all()
        yield flask_app
        app_db.session.remove()
        app_db.drop_all()


@pytest.fixture
def client(app):
    """Test client for the main application."""
    return app.test_client()


@pytest.fixture
def dummy_erp_client():
    """Test client for Dummy_ERP application with in-memory database."""
    dummy_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
    })
    with dummy_app.app_context():
        dummy_db.create_all()
        yield dummy_app.test_client()
        dummy_db.session.remove()
        dummy_db.drop_all()

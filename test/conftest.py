import pytest
from app import create_app
from app.configs.database import db


@pytest.fixture(scope="module")
def app():
    return create_app()


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.testing = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    client = app.test_client()
    with app.app_context():
        db.create_all()
    yield client

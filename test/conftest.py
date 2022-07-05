import pytest
from app import create_app
from app.configs.database import db
from flask_jwt_extended import create_access_token


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    with app.app_context():
        db.create_all()
        app.db = db
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def app_session(app):
    return app.db.session


@pytest.fixture()
def authorization(app):
    user = {
        "username": "kallissin",
        "password": "123456",
        "role": "admin"
    }

    acess_token = create_access_token(user)
    authorization = "Bearer " + acess_token
    return authorization

from test._factories import UserFactory

from app.models.user_model import UserModel
from flask import jsonify


def test_create_user_success(client, app_session):
    payload = {
        "name": "kelvin cantarino",
        "email": "kelvin@email.com",
        "username": "kallissin",
        "password": "123456"
    }

    response = client.post(
        "/api/user", 
        headers={'Content-Type': 'application/json'},
        json=payload,
    )
    user = jsonify(app_session.query(UserModel).first())

    assert response.status_code == 201
    assert response.json == user.json


def test_create_user_failed_with_empty_payload(client, app_session):
    payload = {}
    
    response = client.post(
        "/api/user", 
        headers={'Content-Type': 'application/json'},
        json=payload,
    )
    users = app_session.query(UserModel).all()

    assert len(users) is 0
    assert response.status_code == 400
    assert response.json == {
        'message': [
            'name is required',
            'email is required',
            'username is required',
            'password is required'
        ],
        'status': 'error'
    }


def test_create_user_failed_with_payload_none(client, app_session):
    payload = {
        "name": None,
        "email": None,
        "username": None,
        "password": None
    }

    response = client.post(
        "/api/user",
        headers={'Content-Type': 'application/json'},
        json=payload,
    )
    users = app_session.query(UserModel).all()

    assert len(users) is 0
    assert response.status_code == 400
    assert response.json == {
        'message': [
            'key email must be type str',
            'key name must be type str',
            'key password must be type str',
            'key username must be type str'
        ],
        'status': 'error'
    }


def test_create_user_failed_with_invalid_key(client, app_session):
    payload = {
        "name": "João",
        "mail": "joao@email.com",
        "surname": "Almeida",
        "password": "123456"
    }

    response = client.post(
        "/api/user",
        headers={'Content-Type': 'application/json'},
        json=payload,
    )

    users = app_session.query(UserModel).all()

    assert len(users) is 0
    assert response.status_code == 400
    assert response.json == {
        'message': [
            'key mail invalid', 
            'key surname invalid'
        ], 
        'status': 'error'
    }


def test_create_user_failed_already_username(client, app_session):
    UserFactory(password="123456", username="Almeida")
    
    payload = {
        "name": "João",
        "email": "joao@email.com",
        "username": "Almeida",
        "password": "123456"
    }

    response = client.post(
        "/api/user",
        headers={'Content-Type': 'application/json'},
        json=payload,
    )
    # users = app_session.query(UserModel).all()
    # TODO: Implementar uma forma para a sessão não fechar
    assert response.json == {'message': 'username already exists'}
    assert response.status_code == 409

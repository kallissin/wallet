from flask_jwt_extended import create_access_token
from app import create_app


def test_create_customer(client):
    app = create_app()

    with app.app_context():
        user = {
            "username": "maria",
            "password": "123456",
            "role": "admin"
        }

        access_token = create_access_token(user)
        credentials = {"Authorization": "Bearer " + access_token}

    data = {
        "name": "GusTAvo Reis",
        "cpf": "18095860034"
    }

    res = client.post("/api/customer", json=data, headers=credentials)

    expected = {
        "customer_id": 1,
        "name": "gustavo reis",
        "cpf": "18095860034"
    }

    assert res.get_json() == expected

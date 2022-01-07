from flask_jwt_extended import create_access_token
from app import create_app


def test_status_code_ok_get_all_users(client):
    app = create_app()

    with app.app_context():
        user = {
            "username": "maria",
            "password": "123456",
            "role": "admin"
        }

        access_token = create_access_token(user)
        credentials = {"Authorization": "Bearer " + access_token}

    response = client.get("/api/user", headers=credentials)
    assert response.status_code == 200


def test_status_code_ok_get_user_by_id(client):
    app = create_app()
    with app.app_context():
        data = {
            "name": "MaRia SilvA",
            "email": "maria@email.com",
            "username": "maria",
            "password": "123456"
        }

        client.post("/api/user", json=data, headers={'Content-Type': 'application/json'})

        user = {
            "username": "maria",
            "password": "123456",
            "role": "admin"
        }

        access_token = create_access_token(user)
        credentials = {"Authorization": "Bearer " + access_token}

    response = client.get("/api/user/1", headers=credentials)
    assert response.status_code == 200

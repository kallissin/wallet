from flask_jwt_extended import create_access_token
from app import create_app


def test_status_code_ok_get_all_customers(client):
    app = create_app()

    with app.app_context():
        user = {
            "username": "maria",
            "password": "123456",
            "role": "admin"
        }

        access_token = create_access_token(user)
        credentials = {"Authorization": "Bearer " + access_token}
    url = "/api/customer"
    response = client.get(url, headers=credentials)
    assert response.status_code == 200


def test_status_code_ok_get_customer_by_id(client):
    app = create_app()
    with app.app_context():
        data = {
            "name": "Gustavo Reis",
            "cpf": "18095860034"
        }

        user = {
            "username": "maria",
            "password": "123456",
            "role": "admin"
        }

        access_token = create_access_token(user)
        credentials = {"Authorization": "Bearer " + access_token}

        client.post("/api/customer", json=data, headers=credentials)

    response = client.get("/api/customer/1", headers=credentials)
    assert response.status_code == 200

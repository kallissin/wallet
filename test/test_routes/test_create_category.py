from flask_jwt_extended import create_access_token
from app import create_app


def test_create_category(client):
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
        "name": "bebidas",
        "discount": 0.05
    }

    res = client.post("/api/category", json=data, headers=credentials)

    expected = {
        "category_id": 1,
        "name": "bebidas",
        "discount": 0.05
    }

    assert res.get_json() == expected

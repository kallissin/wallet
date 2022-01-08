from flask_jwt_extended import create_access_token
from app import create_app


def test_create_product(client):
    app = create_app()

    with app.app_context():
        user = {
            "username": "maria",
            "password": "123456",
            "role": "admin"
        }

        access_token = create_access_token(user)
        credentials = {"Authorization": "Bearer " + access_token}

    category = {
        "name": "bebidas",
        "discount": 0.05
    }

    product = {
        "name": "cerveja",
        "category": "Bebidas"
    }

    client.post("/api/category", json=category, headers=credentials)
    res = client.post("/api/product", json=product, headers=credentials)

    expected = {
        "product_id": 1,
        "name": "cerveja",
        "category": {
            "category_id": 1,
            "name": "bebidas",
            "discount": 0.05
        }
    }

    assert res.get_json() == expected

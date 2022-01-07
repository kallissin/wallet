from flask_jwt_extended import create_access_token
from app import create_app


def test_status_code_ok_get_all_products(client):
    app = create_app()

    with app.app_context():
        user = {
            "username": "maria",
            "password": "123456",
            "role": "admin"
        }

        access_token = create_access_token(user)
        credentials = {"Authorization": "Bearer " + access_token}
    url = "/api/product"
    response = client.get(url, headers=credentials)
    assert response.status_code == 200


def test_status_code_ok_get_product_by_id(client):
    app = create_app()
    with app.app_context():
        product = {
            "name": "cerveja",
            "category": "bebidas"
        }

        category = {
            "name": "bebidas",
            "discount": 0.05
        }

        user = {
            "username": "maria",
            "password": "123456",
            "role": "admin"
        }

        access_token = create_access_token(user)
        credentials = {"Authorization": "Bearer " + access_token}

        client.post("/api/category", json=category, headers=credentials)
        client.post("/api/product", json=product, headers=credentials)

    response = client.get("/api/product/1", headers=credentials)
    assert response.status_code == 200

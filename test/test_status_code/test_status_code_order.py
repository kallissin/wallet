from flask_jwt_extended import create_access_token
from app import create_app


def test_status_code_ok_get_all_orders(client):
    app = create_app()

    with app.app_context():
        user = {
            "username": "maria",
            "password": "123456",
            "role": "admin"
        }

        access_token = create_access_token(user)
        credentials = {"Authorization": "Bearer " + access_token}

    response = client.get("/api/order", headers=credentials)
    assert response.status_code == 200


def test_status_code_ok_get_order_by_id(client):
    app = create_app()
    with app.app_context():
        order = {
            "cpf": "18095860034"
        }

        customer = {
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

        client.post("/api/customer", json=customer, headers=credentials)
        client.post("/api/order", json=order, headers=credentials)

    response = client.get("/api/order/1", headers=credentials)
    assert response.status_code == 200


def test_status_code_ok_get_all_itens(client):
    app = create_app()

    with app.app_context():
        user = {
            "username": "maria",
            "password": "123456",
            "role": "admin"
        }

        access_token = create_access_token(user)
        credentials = {"Authorization": "Bearer " + access_token}

    response = client.get("/api/order/item", headers=credentials)
    assert response.status_code == 200


def test_status_code_ok_get_item_by_id(client):
    app = create_app()

    with app.app_context():
        order = {
            "cpf": "18095860034"
        }

        customer = {
            "name": "Gustavo Reis",
            "cpf": "18095860034"
        }

        product = {
            "name": "cerveja",
            "category": "bebidas"
        }

        category = {
            "name": "bebidas",
            "discount": 0.05
        }

        item = {
            "name": "cerveja",
            "value": 2.35,
            "qty": 2
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
        client.post("/api/customer", json=customer, headers=credentials)
        client.post("/api/order", json=order, headers=credentials)
        client.post("/api/order/1/item", json=item, headers=credentials)
    response = client.get("/api/order/item/1", headers=credentials)
    assert response.status_code == 200


def test_status_code_ok_get_item_by_order_id(client):
    app = create_app()

    with app.app_context():
        order = {
            "cpf": "18095860034"
        }

        customer = {
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

        client.post("/api/customer", json=customer, headers=credentials)
        client.post("/api/order", json=order, headers=credentials)
    response = client.get("/api/order/1/item", headers=credentials)
    assert response.status_code == 200

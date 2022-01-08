from flask_jwt_extended import create_access_token
from app import create_app


def test_create_order(client):
    app = create_app()

    with app.app_context():
        user = {
            "username": "maria",
            "password": "123456",
            "role": "admin"
        }

        access_token = create_access_token(user)
        credentials = {"Authorization": "Bearer " + access_token}

    customer = {
        "name": "GusTAvo Reis",
        "cpf": "18095860034"
    }

    order = {
       "cpf": "18095860034"
    }

    client.post("/api/customer", json=customer, headers=credentials)
    res = client.post("/api/order", json=order, headers=credentials)
    sold_at = res.get_json()['sold_at']
    expected = {
        "order_id": 1,
        "sold_at": sold_at,
        "total": None,
        "customer": {
            "customer_id": 1,
            "cpf": "18095860034",
            "name": "gustavo reis"
        },
        "cashback_id": None
    }

    assert res.get_json() == expected


def test_create_item_in_order(client):
    app = create_app()

    with app.app_context():
        user = {
            "username": "maria",
            "password": "123456",
            "role": "admin"
        }

        access_token = create_access_token(user)
        credentials = {"Authorization": "Bearer " + access_token}

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

        client.post("/api/category", json=category, headers=credentials)
        client.post("/api/product", json=product, headers=credentials)
        client.post("/api/customer", json=customer, headers=credentials)
        client.post("/api/order", json=order, headers=credentials)
    res = client.post("/api/order/1/item", json=item, headers=credentials)

    expected = [{
        "item_id": 1,
        "product": {
            "product_id": 1,
            "name": "cerveja",
            "category": "bebidas"
        },
        "value": 2.35,
        "qty": 2
    }]

    assert res.get_json() == expected

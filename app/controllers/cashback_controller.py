from flask import request, jsonify, current_app
from app.models.order_model import OrderModel
import requests


def calculate_discount(value, discount):
    return value * discount


def calculate_cashback(itens):
    total_cashback_amount = 0

    for item in itens:
        value_per_item = item.value * item.qty

        discount_per_item = item.product.category.discount

        value_cashback = calculate_discount(value_per_item, discount_per_item)

        total_cashback_amount += value_cashback

    return total_cashback_amount


def generate_cashback():
    data = request.get_json()

    order = OrderModel.query.filter_by(id=data['order_id']).first_or_404()

    payload = {
        'cashback': calculate_cashback(order.itens),
        'document': order.customer.cpf
    }

    url = "https://5efb30ac80d8170016f7613d.mockapi.io/api/mock/Cashback"

    if not order.cashback_id:
        new_data = requests.post(url, payload)
    else:
        new_data = requests.put(url + '/' + str(order.cashback_id), payload)
    new_data = new_data.json()

    id = new_data['id']

    setattr(order, 'cashback_id', id)

    current_app.db.session.add(order)
    current_app.db.session.commit()

    return jsonify({
        "id": order.id,
        "sold_at": order.sold_at,
        "customer": {
            "customer_id": order.customer.id,
            "cpf": order.customer.cpf,
            "name": order.customer.name
        },
        "total": order.total,
        "itens": order.itens,
        "cashback": {
            "cashback_id": int(new_data['id']),
            "value": float(new_data['cashback'])
        }
    })

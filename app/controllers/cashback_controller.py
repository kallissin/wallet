from http import HTTPStatus
from flask import request, jsonify, current_app
from app.models.order_model import OrderModel
import requests


def calculate_discount(value, discount):
    return round(value * discount, 2)


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

    order = OrderModel.query.filter_by(order_id=data['order_id']).first_or_404()

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

    id = int(new_data['id'])

    setattr(order, 'cashback_id', id)

    current_app.db.session.add(order)
    current_app.db.session.commit()

    return jsonify({
        "order_id": order.order_id,
        "sold_at": order.sold_at,
        "customer": order.customer,
        "total": order.total,
        "itens": [{
            "register_id": item.register_id,
            "product": item.product.name,
            "value": item.value,
            "qty": item.qty
        } for item in order.itens],
        "cashback": {
            "cashback_id": order.cashback_id,
            "value": float(new_data['cashback'])
        }
    })


def get_cashback_by_id(cashback_id):
    url = "https://5efb30ac80d8170016f7613d.mockapi.io/api/mock/Cashback"
    data = requests.get(url + '/' + cashback_id)
    data = data.json()
    if 'id' in data:
        return jsonify(data), HTTPStatus.OK
    return jsonify({"message": "cashback not found"}), HTTPStatus.NOT_FOUND

from flask import request, jsonify
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

    new_data = requests.post(url, payload)

    return jsonify(new_data.json())

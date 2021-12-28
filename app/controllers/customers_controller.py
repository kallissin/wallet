from flask import request, jsonify, current_app
from app.models.customer_model import CustomerModel


def create_customer():
    data = request.get_json()

    customer = CustomerModel(**data)

    current_app.db.session.add(customer)
    current_app.db.session.commit()

    return jsonify(customer)

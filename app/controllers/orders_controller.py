from flask import request, jsonify, current_app
from http import HTTPStatus
from werkzeug.exceptions import NotFound
from app.exceptions.exc import InvalidKeyError, InvalidValueError, RequiredKeyError
from app.models.order_model import OrderModel
from app.models.customer_model import CustomerModel
from app.models.order_product_model import OrderProductModel
from app.models.product_model import ProductModel


def calculate_total_amount(order):
    total = 0
    for item in order.itens:
        value_per_item = item.value * item.qty
    total += value_per_item
    setattr(order, 'total', total)
    return order


def create_order():
    data = request.get_json()
    try:
        OrderModel.validate_key_and_value(data)
        OrderModel.validate_required_key(data)
        customer = CustomerModel.query.filter_by(cpf=data['cpf']).first_or_404()
        order = OrderModel(customer_id=customer.customer_id)

        current_app.db.session.add(order)
        current_app.db.session.commit()

        return jsonify(order), HTTPStatus.CREATED
    except InvalidValueError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except InvalidKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except RequiredKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except NotFound:
        return jsonify({"message": "customer not found"}), HTTPStatus.NOT_FOUND


def get_all_orders():
    list_orders = OrderModel.query.order_by(OrderModel.order_id).all()
    return jsonify(list_orders)


def get_order_by_id(order_id):
    try:
        order = OrderModel.query.filter_by(order_id=order_id).first_or_404()
        return jsonify(order)
    except NotFound:
        return jsonify({"message": "order not found"}), HTTPStatus.NOT_FOUND


def insert_item(order_id):
    data = request.get_json()

    try:
        OrderProductModel.validate_key_and_value(data)
        OrderProductModel.validate_required_key(data)
        product_name = data.pop('name')
        product = ProductModel.query.filter_by(name=product_name).first_or_404()
        item = OrderProductModel(product=product, **data)
    except NotFound:
        return jsonify({"message": "product not found"}), HTTPStatus.NOT_FOUND
    except InvalidValueError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except InvalidKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except RequiredKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    order = OrderModel.query.filter_by(order_id=order_id).first_or_404()
    existing_item = False

    for item_order in order.itens:
        if product_name == item_order.product.name:
            existing_item = True

    if existing_item:
        return jsonify({"message": "Item already exists"}), HTTPStatus.CONFLICT

    order.itens.append(item)
    order = calculate_total_amount(order)
    current_app.db.session.add(order)
    current_app.db.session.commit()

    return jsonify([{
        "item_id": item.register_id,
        "product": {
            "product_id": item.product.product_id,
            "name": item.product.name,
            "category": item.product.category.name
        },
        "value": item.value,
        "qty": item.qty
    } for item in order.itens]), HTTPStatus.CREATED


def get_item_by_id(item_id):
    try:
        item = OrderProductModel.query.filter_by(register_id=item_id).first_or_404()
        return jsonify({
            "item_id": item.register_id,
            "product": {
                "product_id": item.product.product_id,
                "name": item.product.name,
                "category": {
                    "category_id": item.product.category.category_id,
                    "name": item.product.category.name
                }
            },
            "value": item.value,
            "qty": item.qty
        }), HTTPStatus.OK
    except NotFound:
        return jsonify({"message": "item not found"}), HTTPStatus.NOT_FOUND


def get_all_itens():
    list_itens = OrderProductModel.query.order_by(OrderProductModel.register_id).all()
    return jsonify([{
        "item_id": item.register_id,
        "product": {
            "product_id": item.product.product_id,
            "name": item.product.name,
            "category": item.product.category.name
        },
        "value": item.value,
        "qty": item.qty
    } for item in list_itens]), HTTPStatus.OK


def get_item_by_order_id(order_id):
    try:
        order = OrderModel.query.filter_by(order_id=order_id).first_or_404()
        return jsonify([{
            "item_id": item.register_id,
            "product": {
                "product_id": item.product.product_id,
                "name": item.product.name,
                "category": item.product.category.name
            },
            "value": item.value,
            "qty": item.qty
        } for item in order.itens])
    except NotFound:
        return jsonify({"message": "order not found"}), HTTPStatus.NOT_FOUND


def delete_order(order_id):
    try:
        order = OrderModel.query.filter_by(order_id=order_id).first_or_404()
        current_app.db.session.delete(order)
        current_app.db.session.commit()
        return jsonify(""), HTTPStatus.NO_CONTENT
    except NotFound:
        return jsonify({"message": "order not found"}), HTTPStatus.NOT_FOUND


def delete_item(item_id):
    try:
        item = OrderProductModel.query.filter_by(register_id=item_id).first_or_404()
        current_app.db.session.delete(item)
        current_app.db.session.commit()
        return jsonify(""), HTTPStatus.NO_CONTENT
    except NotFound:
        return jsonify({"message": "item not found"}), HTTPStatus.NOT_FOUND


# TODO: implementar a função com as exceções
def update_item(item_id):
    ...

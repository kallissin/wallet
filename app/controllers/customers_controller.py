from flask import request, jsonify, current_app
from app.exceptions.exc import InvalidKeyError, InvalidTypeCpfError, InvalidValueError, RequiredKeyError
from app.models.customer_model import CustomerModel
from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation


def validate_cpf(cpf):
    output = False
    cpf_to_compare = cpf[:-2]

    while len(cpf_to_compare) < 11:
        start = len(cpf_to_compare) + 1
        total = 0

        for index, value in enumerate(cpf_to_compare):
            total += int(value) * (start - index)
       
        digit = str(total * 10 % 11)
        cpf_to_compare += digit

    if cpf == cpf_to_compare:
        output = True
    return output


def create_customer():
    data = request.get_json()
    try:
        CustomerModel.validate_key_and_value(data)
        CustomerModel.validate_required_key(data)
        
        if not validate_cpf(data['cpf']):
            return jsonify({"message": "cpf is not valid"}), HTTPStatus.BAD_REQUEST

        customer = CustomerModel(**data)

        current_app.db.session.add(customer)
        current_app.db.session.commit()

        return jsonify(customer), HTTPStatus.CREATED
    except InvalidValueError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except InvalidKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except RequiredKeyError as err:
        return jsonify(err.message), HTTPStatus.BAD_REQUEST
    except IntegrityError as err:
        if isinstance(err.orig, UniqueViolation):   
            return jsonify({"message": "cpf already exists"}), HTTPStatus.CONFLICT
    except InvalidTypeCpfError as err:
        return jsonify({"message": str(err)}), HTTPStatus.BAD_REQUEST


def get_all_customer():
    customers_list = CustomerModel.query.order_by(CustomerModel.id).all()

    return jsonify(customers_list), HTTPStatus.OK


def get_customer_by_id(customer_id):
    customer = CustomerModel.query.filter_by(id=customer_id).first_or_404()

    return jsonify(customer), HTTPStatus.OK


def update_customer(customer_id):
    data = request.get_json()

    customer = CustomerModel.query.filter_by(id=customer_id).first_or_404()

    for key, value in data.items():
        setattr(customer, key, value)

    current_app.db.session.add(customer)
    current_app.db.session.commit()

    return jsonify(customer), HTTPStatus.OK

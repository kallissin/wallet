from flask import jsonify, request, current_app
from app.models.user_model import UserModel


def create_user():
    data = request.get_json()

    user = UserModel(**data)

    current_app.db.session.add(user)
    current_app.db.session.commit()

    return jsonify(user), 201


def get_all_user():
    users_list = UserModel.query.order_by(UserModel.id).all()
    return jsonify(users_list)

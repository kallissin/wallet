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


def get_user_by_id(user_id):
    user = UserModel.query.filter_by(id=user_id).first_or_404()
    return jsonify(user)


def update_user(user_id):
    data = request.get_json()

    if 'role' in data:
        return jsonify({"message": "Unauthorized to update role"}), 401

    user = UserModel.query.filter_by(id=user_id).first_or_404()

    for key, value in data.items():
        setattr(user, key, value)

    current_app.db.session.add(user)
    current_app.db.session.commit()

    return jsonify(user)


def delete_user(user_id):

    user = UserModel.query.filter_by(id=user_id).first_or_404()
    current_app.db.session.delete(user)
    current_app.db.session.commit()

    return jsonify(""), 204

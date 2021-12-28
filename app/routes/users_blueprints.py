from flask import Blueprint

from app.controllers.users_controller import create_user, get_all_user

bp = Blueprint('user_bp', __name__, url_prefix='/user')

bp.post('')(create_user)
bp.get('')(get_all_user)

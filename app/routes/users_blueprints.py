from flask import Blueprint

from app.controllers.users_controller import create_user, get_all_user, get_user_by_id

bp = Blueprint('user_bp', __name__, url_prefix='/user')

bp.post('')(create_user)
bp.get('')(get_all_user)
bp.get('/<int:user_id>')(get_user_by_id)

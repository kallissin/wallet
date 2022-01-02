from flask import Blueprint

from app.controllers.cashback_controller import generate_cashback, get_cashback_by_id

bp = Blueprint('cashback_bp', __name__, url_prefix='/cashback')

bp.post('')(generate_cashback)
bp.get('/<string:cashback_id>')(get_cashback_by_id)

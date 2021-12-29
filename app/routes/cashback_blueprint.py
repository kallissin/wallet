from flask import Blueprint

from app.controllers.cashback_controller import generate_cashback

bp = Blueprint('cashback_bp', __name__, url_prefix='/cashback')

bp.post('')(generate_cashback)

from flask import Blueprint

from app.controllers.customers_controller import create_customer, get_all_customer, get_customer_by_id

bp = Blueprint('customer_bp', __name__, url_prefix='/customer')

bp.post('')(create_customer)
bp.get('')(get_all_customer)
bp.get('<int:customer_id>')(get_customer_by_id)

from flask import Blueprint

from app.controllers.categories_controller import create_category

bp = Blueprint('category_bp', __name__, url_prefix='category')

bp.post('')(create_category)

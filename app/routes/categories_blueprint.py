from flask import Blueprint
from app.controllers.categories_controller import create_category, get_all_categories, get_category_by_id, update_category


bp = Blueprint('category_bp', __name__, url_prefix='category')

bp.post('')(create_category)
bp.get('')(get_all_categories)
bp.get('/<int:category_id>')(get_category_by_id)
bp.patch('/<int:category_id>')(update_category)

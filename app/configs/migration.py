from flask import Flask
from flask_migrate import Migrate


def init_app(app: Flask): 
    from app.models.user_model import UserModel
    from app.models.customer_model import CustomerModel
    from app.models.category_model import CategoryModel
    from app.models.product_model import ProductModel
    from app.models.order_model import OrderModel
    Migrate(app, app.db)

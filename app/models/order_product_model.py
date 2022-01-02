from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from app.configs.database import db
from dataclasses import dataclass

from app.exceptions.exc import InvalidKeyError, InvalidValueError, RequiredKeyError


@dataclass
class OrderProductModel(db.Model):
    model_to_compare = {
        "name": str,
        "value": float,
        "qty": int,
    }

    register_id: int
    product_id: int
    value: float
    qty: int

    __tablename__ = 'orders_products'

    register_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    value = Column(Float, nullable=False)
    qty = Column(Integer, nullable=False)

    product = relationship('ProductModel')

    @classmethod
    def validate_key_and_value(cls, data: dict):
        for key, value in data.items():
            if key not in cls.model_to_compare:
                raise InvalidKeyError(data, cls.model_to_compare)
            if type(value) != cls.model_to_compare[key]:
                raise InvalidValueError(data, cls.model_to_compare)

    @classmethod
    def validate_required_key(cls, data: dict):
        for key in cls.model_to_compare:
            if key not in data:
                raise RequiredKeyError(data, cls.model_to_compare)

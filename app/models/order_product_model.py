from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from app.configs.database import db
from dataclasses import dataclass


@dataclass
class OrderProductModel(db.Model):
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

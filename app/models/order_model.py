from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from app.configs.database import db
from dataclasses import dataclass
from datetime import datetime
from app.exceptions.exc import InvalidKeyError, InvalidValueError, RequiredKeyError
from .customer_model import CustomerModel


@dataclass
class OrderModel(db.Model):
    model_to_compare = {
        "cpf": str
    }

    order_id: int
    sold_at: str
    total: float
    customer: CustomerModel
    cashback_id: int

    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    sold_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    total = Column(Float)
    cashback_id = Column(Integer)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)

    customer = relationship('CustomerModel', backref='orders', uselist=False)

    itens = relationship('OrderProductModel', cascade='all, delete-orphan')

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

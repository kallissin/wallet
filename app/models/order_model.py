from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from app.configs.database import db
from dataclasses import dataclass
from datetime import datetime
from .customer_model import CustomerModel


@dataclass
class OrderModel(db.Model):
    id: int
    sold_at: str
    total: float
    customer: CustomerModel

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    sold_at = Column(DateTime, default=datetime.utcnow(), nullable=False)
    total = Column(Float, default=0, nullable=False)
    cashback_id = Column(Integer)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)

    customer = relationship('CustomerModel', backref='orders', uselist=False)

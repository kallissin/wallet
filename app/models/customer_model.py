from sqlalchemy import Column, String, Integer
from app.configs.database import db
from dataclasses import dataclass


@dataclass
class CustomerModel(db.Model):
    id: int
    cpf: str
    name: str

    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    cpf = Column(String(11), unique=True, nullable=False)
    name = Column(String(150), nullable=False)

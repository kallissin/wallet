from sqlalchemy import Column, String, Integer, Float
from app.configs.database import db
from dataclasses import dataclass


@dataclass
class CategoryModel(db.Model):
    category_id: int
    name: str
    discount: float

    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    discount = Column(Float, nullable=False)

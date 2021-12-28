from sqlalchemy import Column, String, Integer
from sqlalchemy.sql.schema import ForeignKey
from app.configs.database import db
from dataclasses import dataclass
from .category_model import CategoryModel
from sqlalchemy.orm import relationship


@dataclass
class ProductModel(db.Model):
    id: int
    name: str
    category: CategoryModel

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    category = relationship('CategoryModel', backref='products', uselist=False)

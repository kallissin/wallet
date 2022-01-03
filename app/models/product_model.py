from sqlalchemy import Column, String, Integer
from sqlalchemy.sql.schema import ForeignKey
from app.configs.database import db
from dataclasses import dataclass
from app.exceptions.exc import InvalidKeyError, InvalidValueError, RequiredKeyError
from .category_model import CategoryModel
from sqlalchemy.orm import relationship, validates


@dataclass
class ProductModel(db.Model):
    model_to_compare = {
        "name": str,
        "category": str,
    }

    product_id: int
    name: str
    category: CategoryModel

    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.category_id'), nullable=False)

    category = relationship('CategoryModel', backref='products', uselist=False)

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

    @validates('name')
    def formated_values(self, key, value):
        if key == 'name':
            value = value.lower()
        return value

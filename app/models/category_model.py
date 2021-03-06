from dataclasses import dataclass

from app.configs.database import db
from app.exceptions.exc import (InvalidKeyError, InvalidValueError,
                                RequiredKeyError)
from sqlalchemy import Column, Float, Integer, Unicode
from sqlalchemy.orm import validates


@dataclass
class CategoryModel(db.Model):
    model_to_compare = {
        "name": str,
        "discount": float,
    }

    category_id: int
    name: str
    discount: float

    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    name = Column(Unicode(150), unique=True, nullable=False)
    discount = Column(Float, nullable=False)

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

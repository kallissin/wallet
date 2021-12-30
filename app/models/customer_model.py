from sqlalchemy import Column, String, Integer
from app.configs.database import db
from dataclasses import dataclass

from app.exceptions.exc import InvalidKeyError, InvalidValueError, RequiredKeyError


@dataclass
class CustomerModel(db.Model):
    model_to_compare = {
        "name": str,
        "cpf": str
    }

    customer_id: int
    cpf: str
    name: str

    __tablename__ = 'customers'

    customer_id = Column(Integer, primary_key=True)
    cpf = Column(String(11), unique=True, nullable=False)
    name = Column(String(150), nullable=False)

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

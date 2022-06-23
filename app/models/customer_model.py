import re
from dataclasses import dataclass

from app.configs.database import db
from app.exceptions.exc import (InvalidKeyError, InvalidTypeCpfError,
                                InvalidValueError, RequiredKeyError)
from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.orm import validates


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
    cpf = Column(Unicode(11), unique=True, nullable=False)
    name = Column(Unicode(150), nullable=False)

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

    @validates('cpf')
    def validate_format_cpf(self, key, value):
        regex_cpf = r'^[0-9]{11}$'
        validate = re.fullmatch(regex_cpf, value)

        if len(value) < 11 or len(value) > 11:
            raise (InvalidTypeCpfError("cpf must be 11 digits"))

        if not validate:
            raise (InvalidTypeCpfError("cpf must be in format xxxxxxxxxxx"))
        return value

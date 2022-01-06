from sqlalchemy import Column, String, Integer
from app.configs.database import db
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash
from app.exceptions.exc import InvalidValueError, InvalidKeyError, RequiredKeyError
from sqlalchemy.orm import validates


@dataclass
class UserModel(db.Model):
    model_to_compare = {
        "name": str,
        "email": str,
        "username": str,
        "password": str
    }
    model_to_compare_login = {
        "username": str,
        "password": str
    }

    user_id: int
    name: str
    email: str
    username: str
    role: str

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String, unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default='user', nullable=False)

    @property
    def password(self):
        raise AttributeError('Password is not acessible')

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def check_password(self, password_to_compare):
        return check_password_hash(self.password_hash, password_to_compare)

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

    @classmethod
    def validate_login(cls, data: dict):
        for key in cls.model_to_compare_login:
            if key not in data:
                raise RequiredKeyError(data, cls.model_to_compare_login)

    @validates('name', 'email')
    def formated_values(self, key, value):
        if key == 'name':
            value = value.lower()
        if key == 'email':
            value = value.lower()

        return value

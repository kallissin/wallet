from sqlalchemy import Column, String, Integer
from app.configs.database import db
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash
from app.exceptions.exc import InvalidValueError, InvalidKeyError, RequiredKeyError


@dataclass
class UserModel(db.Model):
    user_id: int
    name: str
    email: str
    username: str
    role: str

    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String, nullable=False)
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

    @staticmethod
    def validate_data(data: dict):
        model_required = ['name', 'email', 'username', 'password']
      
        for key_data, value in data.items():
            if key_data not in model_required:
                raise InvalidKeyError(data)
            if type(value) != str:
                raise InvalidValueError(data)

        for key_model in model_required:
            if key_model not in data:
                raise RequiredKeyError(data)

from sqlalchemy import Column, String, Integer
from app.configs.database import db
from dataclasses import dataclass
from werkzeug.security import generate_password_hash, check_password_hash


@dataclass
class UserModel(db.Model):
    id: int
    name: str
    email: str
    username: str
    role: str

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
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

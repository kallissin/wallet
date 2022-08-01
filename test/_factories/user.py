import factory
from app.configs.database import db
from app.models.user_model import UserModel


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = UserModel
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "commit"

    user_id = factory.Sequence(lambda n: n)
    name = factory.Faker("name", locale="pt_BR")
    email = factory.Faker("email", domain="cashback.com.br")
    username = factory.Faker("user_name")


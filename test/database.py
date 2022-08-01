from app import create_app
from app.configs.database import db

app_client = create_app()
app_client.config.update({"TESTING": True})
app_client.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
app_client.db = db

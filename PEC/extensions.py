from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_principal import Principal
from flask_session import Session


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
principal = Principal()
session = Session()


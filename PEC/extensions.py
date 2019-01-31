from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_principal import Principal
from flask_session import Session

'''Database and migration'''
db = SQLAlchemy()
migrate = Migrate()

'''Login and access''' #TODO Principal
login_manager = LoginManager()
principal = Principal()

'''Server-side user sessions'''
session = Session()


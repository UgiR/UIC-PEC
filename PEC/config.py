import os
from dotenv import load_dotenv, find_dotenv


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(find_dotenv())

    ENV = os.environ.get('FLASK_ENV')
    DEBUG = ENV == 'development'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')


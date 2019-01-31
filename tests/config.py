import os
import datetime as dt
from dotenv import load_dotenv, find_dotenv


class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(find_dotenv())

    '''BASIC FLASK CONFIG'''
    ENV = 'development'
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'sally-sells-sea-shells'

    '''SQLALCHEMY CONFIG'''
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    '''FLASK-SESSION CONFIG'''
    SESSION_TYPE = 'sqlalchemy'
    SESSION_SQLALCHEMY_TABLE = 'sessions'
    SESSION_COOKIE_SECURE = False
    PERMANENT_SESSION_LIFETIME = dt.timedelta(minutes=15)

    '''GITHUB API CONFIG'''
    GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')


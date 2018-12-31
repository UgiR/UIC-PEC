import pytest
from .factories import UserFactory
from PEC.app import create_app
from PEC.extensions import db as _db


@pytest.fixture
def app():
    _app = create_app('tests.config.Config')
    context = _app.test_request_context()
    context.push()

    yield _app

    context.pop()


@pytest.fixture
def db(app):
    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def user(db):
    user = UserFactory(password='password')
    db.session.commit()
    return user

import pytest
from webtest import TestApp
from .factories import UserFactory, ProjectFactory
from PEC.app import create_app
from PEC.extensions import db as db_


@pytest.fixture
def app():
    _app = create_app('tests.config.Config')
    context = _app.test_request_context()
    context.push()

    yield _app

    context.pop()


@pytest.fixture
def webapp(app):
    return TestApp(app)


@pytest.fixture
def db(app):
    with app.app_context():
        db_.create_all()

    yield db_

    db_.session.close()
    db_.drop_all()


@pytest.fixture
def user(db):
    user_ = UserFactory(password='password')
    db.session.commit()
    return user_


@pytest.fixture
def project(db):
    project_ = ProjectFactory()
    db.session.commit()
    return project_

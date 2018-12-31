import pytest
import datetime as dt
from PEC.user.models import User, Role
from tests.factories import UserFactory


@pytest.mark.usefixtures('db')
class TestUser:
    def test_get_by_id(self):
        user = User('username', 'email@email.com')
        user.save()
        retrieved = User.query.get(user.id)
        assert retrieved == user

    def test_create_at_defaults_to_datetime(self):
        user = User('username', 'email@email.com')
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_factory(self, db):
        user = UserFactory(password='password123')
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.first_name)
        assert bool(user.last_name)
        assert user.active is False
        assert user.check_password('password123')

    def test_check_password(self):
        user = UserFactory(password='password123')
        assert user.check_password('password123') is True
        assert user.check_password('password12') is False

    def test_password_hash(self):
        user = UserFactory(password='password123')
        assert user.password is not 'password123'

    def test_set_password(self):
        user = UserFactory(password='password123')
        assert user.check_password('password123')
        user.set_password('different_password')
        assert user.check_password('password123') is False
        assert user.check_password('different_password') is True

    def test_roles(self):
        role = Role('admin')
        role.save()
        user = UserFactory()
        user.roles.append(role)
        user.save()
        assert role in user.roles

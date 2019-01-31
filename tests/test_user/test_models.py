import pytest
from uuid import UUID
import datetime as dt
from tests.factories import UserFactory
from PEC.user.models import User
from PEC.public.forms import RegisterForm


@pytest.mark.usefixtures('db')
class TestUser:

    def test_factory(self, db):
        user = UserFactory()
        db.session.commit()
        assert bool(user.email)
        assert bool(user.first_name)
        assert bool(user.last_name)
        assert user.active is False
        assert user.check_password('password')

    def test_get_by_id(self, user):
        retrieved = User.query.get(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self, user):
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_uuid_defaults_unique(self, db):
        user1 = UserFactory()
        user2 = UserFactory()
        user1.save()
        user2.save()
        assert user1.uuid is not user2.uuid
        assert isinstance(user1.uuid, UUID)

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

    def test_roles(self, user):
        user.add_role('USER', 'MODERATOR')
        user.save()
        assert user.has_role()
        assert user.has_role('USER', 'MODERATOR')
        assert not user.has_role('USER', 'ADMIN')

    def test_courses(self, user):
        assert len(user.courses) == 0
        user.add_course('CS111', 'CS141', 'CS151')
        user.save()
        assert user.has_course()
        assert user.has_course('CS111')
        assert user.has_course('CS111', 'CS141', 'CS151')
        assert not user.has_course('CS111', 'CS251')

    def test_skills(self, user):
        assert len(user.skills) == 0
        user.add_skill('PYTHON', 'FLASK', 'BOOTSTRAP')
        user.save()
        assert user.has_skill()
        assert user.has_skill('FLASK')
        assert user.has_skill('PYTHON', 'FLASK', 'BOOTSTRAP')
        assert not user.has_skill('PYTHON', 'JAVASCRIPT')

    def test_from_form(self):
        form = RegisterForm()
        form.first_name.data = 'Joe'
        form.last_name.data = 'Lock'
        form.email.data = 'joe@mail.com'
        form.password.data = 'password123'
        user = User.from_register_form(form)
        assert user.first_name == form.first_name.data
        assert user.last_name == form.last_name.data
        assert user.email == form.email.data
        assert user.check_password(form.password.data)

    def test_exists(self, user):
        assert User.exists() is False
        assert User.exists(email=user.email)
        assert User.exists(email=user.email, first_name=user.first_name, last_name=user.last_name)
        assert User.exists(first_name=user.first_name, last_name=user.last_name)
        assert User.exists(uuid=user.uuid)
        user.delete()
        assert not User.exists(email=user.email)
        assert not User.exists(email=user.email, first_name=user.first_name, last_name=user.last_name)
        assert not User.exists(first_name=user.first_name, last_name=user.last_name)
        assert not User.exists(uuid=user.uuid)
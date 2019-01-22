import pytest
from uuid import UUID
import datetime as dt
from tests.factories import UserFactory
from PEC.user.models import User
from PEC.user.attributes import Role as Role_
from PEC.user.attributes import Skill as Skill_
from PEC.user.attributes import Course as Course_
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
        #user.add_role(Role.USER, Role.MODERATOR)
        user.add_attribute(roles=[Role_.USER, Role_.MODERATOR])
        user.save()
        assert user.has_role()
        assert user.has_role(Role_.USER, Role_.MODERATOR)
        assert not user.has_role(Role_.USER, Role_.ADMIN)

    def test_courses(self, user):
        assert len(user.courses) == 0
        #user.add_course(Course.CS111, Course.CS141, Course.CS151)
        user.add_attribute(courses=[Course_.CS111, Course_.CS141, Course_.CS151])
        user.save()
        assert user.has_course()
        assert user.has_course(Course_.CS111)
        assert user.has_course(Course_.CS111, Course_.CS141, Course_.CS151)
        assert not user.has_course(Course_.CS111, Course_.CS251)

    def test_skills(self, user):
        assert len(user.skills) == 0
        user.add_skill(Skill_.PYTHON, Skill_.FLASK, Skill_.BOOTSTRAP)
        user.save()
        assert user.has_skill()
        assert user.has_skill(Skill_.FLASK)
        assert user.has_skill(Skill_.PYTHON, Skill_.FLASK, Skill_.BOOTSTRAP)
        assert not user.has_skill(Skill_.PYTHON, Skill_.JAVASCRIPT)

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
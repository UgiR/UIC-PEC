import pytest
import datetime as dt
from uuid import UUID
from PEC.user.models import User, Role
from PEC.user.attributes import Role, Course, Skill
from tests.factories import UserFactory


@pytest.mark.usefixtures('db')
class TestUser:

    def test_factory(self, db):
        user = UserFactory(password='password123')
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.first_name)
        assert bool(user.last_name)
        assert user.active is False
        assert user.check_password('password123')

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
        user.add_role(Role.USER, Role.MODERATOR)
        user.save()
        assert user.has_role()
        assert user.has_role(Role.USER, Role.MODERATOR)
        assert not user.has_role(Role.USER, Role.ADMIN)

    def test_courses(self, user):
        assert len(user.courses) == 0
        user.add_course(Course.CS111, Course.CS141, Course.CS151)
        user.save()
        assert user.has_course()
        assert user.has_course(Course.CS111)
        assert user.has_course(Course.CS111, Course.CS141, Course.CS151)
        assert not user.has_course(Course.CS111, Course.CS251)

    def test_skills(self, user):
        assert len(user.skills) == 0
        user.add_skill(Skill.PYTHON, Skill.FLASK, Skill.BOOTSTRAP)
        user.save()
        assert user.has_skill()
        assert user.has_skill(Skill.FLASK)
        assert user.has_skill(Skill.PYTHON, Skill.FLASK, Skill.BOOTSTRAP)
        assert not user.has_skill(Skill.PYTHON, Skill.JAVASCRIPT)

from factory import PostGenerationMethodCall, Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory
from PEC.database import db
from PEC.user.models import User
from PEC.project.models import Project
from PEC.project.attributes import Status


class BaseFactory(SQLAlchemyModelFactory):

    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    class Meta:
        model = User

    email = Sequence(lambda n: 'user{0}@example.com'.format(n))
    password = PostGenerationMethodCall('set_password', 'password')
    first_name = "Joe"
    last_name = "Lock"


class ProjectFactory(BaseFactory):
    class Meta:
        model = Project

    title = Sequence(lambda n: 'project_{}'.format(n))
    description = "This is a description."
    status = Status.development
    user = SubFactory(UserFactory)

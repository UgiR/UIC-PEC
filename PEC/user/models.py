import datetime as dt
import uuid
from hashlib import md5
from flask_login import UserMixin
from sqlalchemy_utils import UUIDType
from werkzeug.security import generate_password_hash, check_password_hash
from PEC.database import db, CRUDMixin, UserAttributeModel, BaseModel
from PEC.extensions import login_manager
from .attributes import Course as Course_
from .attributes import Skill as Skill_
from .attributes import Role as Role_


"""Relation table mapping users to roles"""
roles_users = db.Table('roles_users',
                       db.Column('users_id', db.Integer(), db.ForeignKey('users.id')),
                       db.Column('roles_id', db.Integer(), db.ForeignKey('roles.id'))
                       )


class Role(UserAttributeModel):
    __tablename__ = 'roles'
    name = db.Column(db.Enum(Role_))


"""Relation table mapping users to their chosen course attributes"""
courses_users = db.Table('courses_users',
                         db.Column('users_id', db.Integer(), db.ForeignKey('users.id')),
                         db.Column('courses_id', db.Integer(), db.ForeignKey('courses.id'))
                         )


class Course(UserAttributeModel):
    __tablename__ = 'courses'
    name = db.Column(db.Enum(Course_))


"""Relation table mapping users to their chosen skill attributes"""
skills_users = db.Table('skills_users',
                        db.Column('users_id', db.Integer(), db.ForeignKey('users.id')),
                        db.Column('skills_id', db.Integer(), db.ForeignKey('skills.id'))
                        )


class Skill(UserAttributeModel):
    __tablename__ = 'skills'
    name = db.Column(db.Enum(Skill_))


class User(UserMixin, CRUDMixin, BaseModel):

    __tablename__ = 'users'
    uuid = db.Column(UUIDType(), nullable=False, unique=True, index=True, default=uuid.uuid4)
    email = db.Column(db.String(80), index=True, unique=True)
    password = db.Column(db.String(128))
    active = db.Column(db.Boolean(), default=False)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    github_id = db.Column(db.Integer(), unique=True, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow())
    last_login_at = db.Column(db.DateTime)
    projects = db.relationship('Project', backref='user', lazy=True)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    courses = db.relationship('Course', secondary=courses_users, backref=db.backref('users', lazy='dynamic'))
    skills = db.relationship('Skill', secondary=skills_users, backref=db.backref('users', lazy='dynamic'))

    # Preserve **kwargs for Model constructor
    def __init__(self, email, password=None, **kwargs):
        db.Model.__init__(self, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    @classmethod
    def from_register_form(cls, form, validate=False):
        """ Creates a User object based on a regsitration form

        :param form: PEC.public.forms.RegisterForm
        :param validate: Whether form should be validated before creating object, defaults to False
        :return: User object or None is validation fails
        """
        if validate:
            if not form.validate():
                return None
        user = cls(form.email.data, form.password.data)
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        return user

    @classmethod
    def exists(cls, **kwargs):
        """ Checks if user with given values exists in the database

        Usage:
            if User.exists(first_name='Joe', last_name='Smith'):
                print('Account with name Joe Smith exists!')

        :return: True if user exists, False otherwise
        """
        if not kwargs:
            return False
        u = cls.query.filter_by(**kwargs).first()
        if u is None:
            return False
        return True

    def avatar(self, size):
        """ Generates a link to a Gravatar profile image

        :param size: Size of avatar image
        :return: URL to gravatar image
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def add_skill(self, *args):
        """ Adds skill attributes to user.
        Valid skills are enumerated in PEC.user.attributes.Skill

        Usage:
            user.add_skill('HTML')
            user.add_skill('REACT', 'PERL', 'PHOTOSHOP')

            skills_to_add = ['HTML', 'FLASK', 'JAVASCRIPT', 'CSS']
            user.add_skill(*skills_to_add)

        :param args: Skills (as strings) to add
        :raises KeyError if invalid skill provided
        :return:
        """
        for skill_name in args:
            skill_ = Skill.get(name=Skill_[skill_name])
            if skill_ not in self.skills:
                self.skills.append(skill_)

    def has_skill(self, *args):
        """ Checks if user has all provided skills.
        Valid skills are enumerated in PEC.user.attributes.Skill

        Usage:
            if user.has_skill('HTML'):
                print('User knows HTML')

            if user.has_skill('REACT', 'PERL', 'PHOTOSHOP'):
                print('User knows React, Perl, and Photoshop')

            skills_to_check = ['HTML', 'FLASK', 'JAVASCRIPT', 'CSS']
            if user.has_skill(*skills_to_check):
                print('User knows HTML, Flask, Javascript, and CSS')


        :param args: Skills (as strings) to check
        :raises KeyError if invalid skill provided
        :return: True if user has all provided skills, False otherwise
        """
        for skill_name in args:
            skill_ = Skill.get(name=Skill_[skill_name])
            if skill_ not in self.skills:
                return False
        return True

    def add_course(self, *args):
        """ Adds course attributes to user.
        Valid courses are enumerated in PEC.user.attributes.Course

        Usage:
            user.add_course('CS111')
            user.add_course('CS141', 'CS151', 'CS211')

            courses_to_add = ['CS251', 'CS261', 'CS301', 'CS341']
            user.add_course(*courses_to_add)

        :param args: Courses (as strings) to add
        :raises KeyError if invalid course provided
        :return:
        """
        for course_name in args:
            course_ = Course.get(name=Course_[course_name])
            if course_ not in self.courses:
                self.courses.append(course_)

    def has_course(self, *args):
        """ Checks if user has all provided courses.
        Valid courses are enumerated in PEC.user.attributes.Course

        Usage:
            if user.has_course('CS111'):
                print('User has taken CS111')
            if user.has_course('CS141', 'CS151', 'CS211'):
                print('User has taken CS141, CS151, and CS211')

            courses_to_check = ['CS251', 'CS261', 'CS301', 'CS341']
            if user.has_course(*courses_to_check):
                print('User has taken CS251, CS261, CS301, and CS341')

        :param args: Skills (as strings) to check
        :raises KeyError if invalid skill provided
        :return: True if user has all provided skills, False otherwise
        """
        for course_name in args:
            course_ = Course.get(name=Course_[course_name])
            if course_ not in self.courses:
                return False
        return True

    def add_role(self, *args):
        """ Adds role attribute to user
        Valid roles are enumerated in PEC.user.attributes.Role

        Usage:
            user.add_role('USER')
            user.add_role('USER', 'MODERATOR')

        :param args: Roles (as strings) to add
        :return:
        """
        for role_name in args:
            role_ = Role.get(name=Role_[role_name])
            self.roles.append(role_)

    def has_role(self, *args):
        """ Checks if user has all provided roles
        Valid roles are enumerated in PEC.user.attributes.Role

        Usage:
            if user.has_role('USER'):
                print('User has User role')
            if user.has_role('USER', 'MODERATOR'):
                print('User has User and Moderator role')

        :param args: Roles (as strings) to check
        :return: True if user has all provided roles, False otherwise
        """
        for role_name in args:
            role_ = Role.get(name=Role_[role_name])
            if role_ not in self.roles:
                return False
        return True

    def set_password(self, password):
        """ Sets the user password

        Usage:
            user.set_password('strongpassword123')

        :param password: String
        :return:
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """ Compares given password against the hashed password

        Usage:
            if user.check_password('strongpassword123'):
                print('Correct password!')

        :param password: String
        :return: True if password is correct, False otherwise
        """
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.email)


@login_manager.user_loader
def load_user(id_):
    return User.query.get(int(id_))

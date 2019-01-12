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
    username = db.Column(db.String(80), index=True, unique=True)
    email = db.Column(db.String(80), index=True, unique=True)
    password = db.Column(db.String(128))
    active = db.Column(db.Boolean(), default=False)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow())
    last_login_at = db.Column(db.DateTime)
    projects = db.relationship('Project', backref='user', lazy=True)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    courses = db.relationship('Course', secondary=courses_users, backref=db.backref('users', lazy='dynamic'))
    skills = db.relationship('Skill', secondary=skills_users, backref=db.backref('users', lazy='dynamic'))

    # Preserve **kwargs for Model constructor
    def __init__(self, username, email, password=None, **kwargs):
        db.Model.__init__(self, username=username, email=email, **kwargs)
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
        user = cls(form.username, form.email, form.password)
        user.first_name = form.first_name
        user.last_name = form.last_name
        return user

    def validate(self):
        u = User.query.filter_by(username=self.username).first()
        if u is not None:
            return False
        u = User.query.filter_by(email=self.email).first()
        if u is not None:
            return False
        return True

    def avatar(self, size):
        """

        :param size: Size of avatar image
        :return: URL to gravatar image
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def add_skill(self, *args):
        for skill in args:
            skill_ = Skill.get(name=skill)
            if skill_ not in self.skills:
                self.skills.append(skill_)

    # TODO Better way to write this function
    # Default arguments are empty tuples, in order to have immutable empty iterables
    # Empty lists as default arguments are static and can cause issues
    def add_attribute(self, skills=(), courses=(), roles=()):
        for skill in skills:
            skill_ = Skill.get(name=skill)
            if skill_ not in self.skills:
                self.skills.append(skill_)
        for course in courses:
            course_ = Course.get(name=course)
            if course_ not in self.courses:
                self.courses.append(course_)
        for role in roles:
            role_ = Role.get(name=role)
            if role_ not in self.roles:
                self.roles.append(role_)

    def has_skill(self, *args):
        for skill in args:
            skill_ = Skill.get(name=skill)
            if skill_ not in self.skills:
                return False
        return True

    def add_course(self, *args):
        for course in args:
            course_ = Course.get(name=course)
            if course_ not in self.courses:
                self.courses.append(course_)

    def has_course(self, *args):
        for course in args:
            course_ = Course.get(name=course)
            if course_ not in self.courses:
                return False
        return True

    def add_role(self, *args):
        for role in args:
            role_ = Role.get(name=role)
            self.roles.append(role_)

    def has_role(self, *args):
        for role in args:
            role_ = Role.get(name=role)
            if role_ not in self.roles:
                return False
        return True

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login_manager.user_loader
def load_user(_id):
    return User.query.get(int(_id))

from flask_login import UserMixin
from sqlalchemy_utils import UUIDType
from werkzeug.security import generate_password_hash, check_password_hash
from PEC.database import db, CRUDMixin, UserAttribute
from PEC.extensions import login_manager
from .attributes import Course as Course_
from .attributes import Skill as Skill_
from .attributes import Role as Role_
import datetime as dt
import uuid


roles_users = db.Table('roles_users',
                       db.Column('users_id', db.Integer(), db.ForeignKey('users.id')),
                       db.Column('roles_id', db.Integer(), db.ForeignKey('roles.id'))
                       )


class Role(UserAttribute, db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    role = db.Column(db.Enum(Role_))
    description = db.Column(db.String(255))

    # Preserve **kwargs for Model constructor
    def __init__(self, name, description='', **kwargs):
        db.Model.__init__(self, name=name, description=description, **kwargs)

    def __repr__(self):
        return '<Role {}'.format(self.name)


courses_users = db.Table('courses_users',
                         db.Column('users_id', db.Integer(), db.ForeignKey('users.id')),
                         db.Column('courses_id', db.Integer(), db.ForeignKey('courses.id'))
                         )


class Course(UserAttribute, db.Model):

    __tablename__ = 'courses'
    id = db.Column(db.Integer(), primary_key=True)
    course = db.Column(db.Enum(Course_))


skills_users = db.Table('skills_users',
                        db.Column('users_id', db.Integer(), db.ForeignKey('users.id')),
                        db.Column('skills_id', db.Integer(), db.ForeignKey('skills.id'))
                        )


class Skill(UserAttribute, db.Model):

    __tablename__ = 'skills'
    id = db.Column(db.Integer(), primary_key=True)
    skill = db.Column(db.Enum(Skill_))


class User(UserMixin, CRUDMixin, db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUIDType(), nullable=False, unique=True, index=True, default=uuid.uuid4)
    username = db.Column(db.String(80), index=True, unique=True)
    email = db.Column(db.String(80), index=True, unique=True)
    password = db.Column(db.String(128))
    active = db.Column(db.Boolean(), default=False)
    first_name = db.Column(db.String(30), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow())
    last_login_at = db.Column(db.DateTime)
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
    def from_register_form(cls, form, validate=True):
        if validate:
            if not form.validate():
                return False
        user = User(form.username, form.email, form.password)
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

    def add_skill(self, skill):
        self.skills.append(Skill.get(skill=skill))

    def add_course(self, course):
        self.courses.append(Course.get(course=course))

    def add_role(self, role):
        self.roles.append(Role.get(role=role))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login_manager.user_loader
def load_user(_id):
    return User.query.get(int(_id))

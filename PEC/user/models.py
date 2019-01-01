from flask_security import UserMixin, RoleMixin
import sqlalchemy_utils
from sqlalchemy_utils import UUIDType
from werkzeug.security import generate_password_hash, check_password_hash
from PEC.database import db, CRUDMixin
from PEC.extensions import login_manager
import datetime as dt
import uuid


roles_users = db.Table('roles_users',
                       db.Column('users_id', db.Integer(), db.ForeignKey('users.id')),
                       db.Column('roles_id', db.Integer(), db.ForeignKey('roles.id'))
                       )


class Role(RoleMixin, CRUDMixin, db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # Preserve **kwargs for Model constructor
    def __init__(self, name, description='', **kwargs):
        db.Model.__init__(self, name=name, description=description, **kwargs)

    def __repr__(self):
        return '<Role {}'.format(self.name)


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

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login_manager.user_loader
def load_user(_id):
    return User.query.get(int(_id))

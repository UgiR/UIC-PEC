from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from PEC.user.models import User


class LoginForm(FlaskForm):

    email = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def validate(self):
        initial_validatation = super(LoginForm, self).validate()
        if not initial_validatation:
            return False
        self.user = User.query.filter_by(email=self.email.data).first()
        if self.user is None:
            self.email.errors.append('User does not exist')
            return False
        if not self.user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False
        return True


class RegisterForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired, Length(min=3, max=25)])
    first_name = StringField('First name')
    last_name = StringField('Last name')
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    password_confirm = PasswordField('Verify password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        self.user = User.query.filter_by(username=self.username.data).first()
        if self.user:
            self.username.errors.append('Choose a different username')
            return False
        self.user = User.query.filter_by(email=self.email.data)
        if self.user:
            self.email.errors.append('Email already registered')
            return False
        return True


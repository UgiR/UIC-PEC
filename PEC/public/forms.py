from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from PEC.user.models import User


class LoginForm(FlaskForm):
    """ Form to be used in login """
    email = StringField('Username', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

    def __init__(self, *args, **kwargs):
        super(LoginForm , self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """ Checks for required fields and checks login credentials and activation status.
        The queried account is stored in self.user

        :return: True if credentials are correct and the user account is active, False otherwise
        """
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
        if not self.user.active:
            self.email.errors.append('User not active')
            return False
        return True


class RegisterForm(FlaskForm):
    """ Form to be used in user registration """
    first_name = StringField('First name', validators=[Length(max=30)])
    last_name = StringField('Last name', validators=[Length(max=30)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    password_confirm = PasswordField('Verify password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """ Checks for required fields and queries for duplicate email/username

        :return: True if username/email unique, False otherwise
        """
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        self.user = User.query.filter_by(email=self.email.data).first()
        if self.user:
            self.email.errors.append('Email already registered')
            return False
        return True


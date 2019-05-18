from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, PasswordField
from wtforms.widgets import CheckboxInput, ListWidget
from wtforms.validators import Email, Length, DataRequired, EqualTo
from PEC.user.models import User
from PEC.user.attributes import Course as Course_
from PEC.user.attributes import Skill as Skill_


class AccountDetailForm(FlaskForm):
    """ Form to be used in changing account details """
    first_name = StringField('First name', validators=[Length(max=30)])
    last_name = StringField('Last name', validators=[Length(max=30)])
    email = StringField('Email addess', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate(self):
        """ Checks that updated information does not conflict with other users in DB

        :return: True if updated email is unique, False otherwise
        """
        initial_validation = super(AccountDetailForm, self).validate()
        if not initial_validation:
            return False
        u = User.query.filter_by(email=current_user.email).first()
        if u is None or u == current_user:
            return True
        self.email.errors.append('Email address already in use')
        return False


class PortfolioForm(FlaskForm):
    """ Form to be used in changing accout portfolio """
    course_selection = SelectMultipleField('Completed Coursework',
                                           option_widget=CheckboxInput(),
                                           widget=ListWidget(prefix_label=False),
                                           choices=Course_.to_choices())
    skill_selection = SelectMultipleField('Skills',
                                          option_widget=CheckboxInput(),
                                          widget=ListWidget(prefix_label=False),
                                          choices=Skill_.to_choices())
    submit = SubmitField('Update')


class UpdatePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6, max=40)])
    new_password_confirm = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Update Password')

    def validate(self):
        initial_validation = super(UpdatePasswordForm, self).validate()
        if not initial_validation:
            return False
        u = User.query.filter_by(email=current_user.email).first()
        return u.check_password(self.current_password)
from flask_login import current_user
from flask_wtf import FlaskForm
from PEC.user.models import User
from wtforms import StringField, SubmitField
from wtforms.validators import Email, Length, DataRequired


class AccountDetailForm(FlaskForm):
    first_name = StringField('First name', validators=[Length(max=30)])
    last_name = StringField('Last name', validators=[Length(max=30)])
    email = StringField('Email addess', validators=[DataRequired(), Email()])
    submit = SubmitField('Update')

    def validate(self):
        initial_validation = super(AccountDetailForm, self).validate()
        if not initial_validation:
            return False
        u = User.query.filter_by(email=self.email.data).first()
        if u is None or u == current_user:
            return True
        self.email.errors.append('Email address already in use')
        return False

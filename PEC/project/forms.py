from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import ListWidget, CheckboxInput
from . import MAX_LENGTH_TITLE, MAX_LENGTH_DESCRIPTION
from PEC.user.attributes import Skill as Skill_


class NewProjectForm(FlaskForm):
    """ Form to be used in new project creation."""
    title = StringField('Project Title', validators=[DataRequired(), Length(max=MAX_LENGTH_TITLE)])
    description = TextAreaField('Project Description', validators=[Length(max=MAX_LENGTH_DESCRIPTION)])
    skill_selection = SelectMultipleField('Preferred Skills',
                                          option_widget=CheckboxInput(),
                                          widget=ListWidget(prefix_label=False),
                                          choices=Skill_.to_choices())
    submit = SubmitField('Submit')

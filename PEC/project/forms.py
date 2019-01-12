from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import ListWidget, CheckboxInput
from . import MAX_LENGTH_TITLE, MAX_LENGTH_DESCRIPTION
from PEC.user.attributes import Skill


class NewProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(), Length(max=MAX_LENGTH_TITLE)])
    description = TextAreaField('Project Description', validators=[Length(max=MAX_LENGTH_DESCRIPTION)])
    skill_selection = SelectMultipleField('Preferred Skills',
                                          option_widget=CheckboxInput(),
                                          widget=ListWidget(prefix_label=False),
                                          choices=Skill.to_choices())
    submit = SubmitField('Submit')

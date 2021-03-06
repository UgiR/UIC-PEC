import datetime as dt
import uuid
from sqlalchemy_utils import UUIDType
from PEC.database import db, CRUDMixin
from .attributes import Status as Status_
from PEC.user.models import Skill
from . import MAX_LENGTH_TITLE, MAX_LENGTH_DESCRIPTION


"""Relation table mapping project preferred skill attributes"""
skills_projects = db.Table('skills_projects',
                           db.Column('projects_id', db.Integer(), db.ForeignKey('projects.id')),
                           db.Column('skills_id', db.Integer(), db.ForeignKey('skills.id'))
                          )

"""Relation table mapping project ownership"""
users_projects = db.Table('users_projects',
                          db.Column('projects_id', db.Integer(), db.ForeignKey('projects.id')),
                          db.Column('users_id', db.Integer(), db.ForeignKey('users.id'))
                          )


class Project(CRUDMixin, db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer(), primary_key=True)
    github_id = db.Column(db.Integer(), unique=True, nullable=True)
    uuid = db.Column(UUIDType(), nullable=False, unique=True, index=True, default=uuid.uuid4)
    title = db.Column(db.String(MAX_LENGTH_TITLE), nullable=False)
    description = db.Column(db.String(MAX_LENGTH_DESCRIPTION), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    status = db.Column(db.Enum(Status_), nullable=False)
    contributors = db.relationship('User', secondary=users_projects, backref=db.backref('contribution_projects', lazy='dynamic'))
    pref_skills = db.relationship('Skill', secondary=skills_projects, backref=db.backref('projects', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @classmethod
    def from_project_form(cls, form, validate=False):
        """ Creates and returns a project object from a NewProjectForm

        :param form: PEC.project.forms.NewProjectForm
        :param validate: Whether the form should be validated before creating object, default False
        :return: Project object or None if validation fails
        """
        if validate:
            if not form.validate():
                return None
        project = cls()
        project.title = form.title.data
        project.description = form.description.data
        return project

    def mark_proposal(self, commit=True):
        """ Changes project status to Proposal #TODO Project status

        :param commit: Change to be committed to database, defaults to True
        :return:
        """
        self.update(status=Status_.proposal, commit=commit)

    def mark_development(self, commit=True):
        """ Changes project status to Development #TODO Project status

        :param commit: Changes to be committed to database, defaults to True
        :return:
        """
        self.update(status=Status_.development, commit=commit)

    def add_pref_skills(self, *args):
        """ Adds given user skill attributes to the list or preferred skills in the project
        Valid skills enumerated in PEC.user.attributes.Skill

        Usage:
            project.add_pref_skills('HTML', 'CSS')

            skills_to_add = ['HTML', 'CSS']
            project.add_pref_skills(*skills_to_add)

        :param args: Skills (as strings)
        :raises KeyError if invalid skill provided
        :return: None
        """
        for skill in args:
            skill_ = Skill.get(name=skill)
            if skill_ not in self.pref_skills:
                self.pref_skills.append(skill_)

    def has_pref_skills(self, *args):
        """ Checks if project contains all given preferred skills
        Valid skills enumerated in PEC.user.attributes.Skill

        Usage:
            if project.has_pref_skills('HTML', 'CSS'):
                print('The project prefers HTML and CSS skills')

            skills_to_check = ['HTML', 'CSS']
            if project.has_pref_skill(*skills_to_check):
                print('The project prefers HTML and CSS skills')

        :param args: PEC.user.attributes.Skill
        :raises KeyError if invalid skill provided
        :return: True if ALL skills are preferred, False otherwise
        """
        for skill in args:
            skill_ = Skill.get(name=skill)
            if skill_ not in self.pref_skills:
                return False
        return True

    def __repr__(self):
        return '<Project {}>'.format(self.uuid)

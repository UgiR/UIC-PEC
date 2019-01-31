import pytest
import datetime as dt
from uuid import UUID
from PEC.user.models import User
from PEC.project.models import Project
from tests.factories import ProjectFactory


@pytest.mark.usefixtures('db')
class TestProject:

    def test_factory(self, db):
        project = ProjectFactory()
        db.session.commit()
        assert bool(project.title)
        project_owner = project.user
        assert isinstance(project_owner, User)
        assert project.user_id == project_owner.id

    def test_get_by_id(self, project):
        retrieved = Project.query.get(project.id)
        assert retrieved == project

    def test_created_at_defaults_to_datetime(self, project):
        assert bool(project.created_at)
        assert isinstance(project.created_at, dt.datetime)

    def test_uuid_defaults_unique(self):
        proj1 = ProjectFactory()
        proj2 = ProjectFactory()
        proj1.save()
        proj2.save()
        assert proj1.uuid is not proj2.uuid
        assert isinstance(proj1.uuid, UUID)

    def test_pref_skills(self, project):
        assert len(project.pref_skills) == 0
        project.add_pref_skills('PYTHON', 'FLASK', 'BOOTSTRAP')
        project.save()
        assert project.has_pref_skills()
        assert project.has_pref_skills('PYTHON')
        assert project.has_pref_skills('PYTHON', 'FLASK', 'BOOTSTRAP')
        assert not project.has_pref_skills('PYTHON', 'JAVASCRIPT')

    def test_contributors(self, project, user):
        assert len(project.contributors) == 0
        project.contributors.append(user)
        project.save()
        user.save()
        assert user in project.contributors
        assert project in user.contribution_projects


import pytest
from PEC import commands
from PEC.user.models import User


@pytest.mark.usefixtures('db')
class TestUserGroup:

    def test_user_create(self, app):
        runner = app.test_cli_runner()
        assert User.query.filter_by(email='test@testing.com').first() is None
        skills = ['-s', 'JAVA', '-s', 'HTML']
        courses = ['-c', 'CS111', '-c', 'CS151']
        options = ['test@testing.com', '-f', 'Joe', '-l', 'Smith']
        options += skills
        options += courses
        result = runner.invoke(commands.create_user, options, input='pass123\npass123\n')
        assert not result.exception
        user = User.query.filter_by(email='test@testing.com').first()
        assert user is not None
        assert user.email == 'test@testing.com'
        assert user.check_password('pass123')
        assert user.first_name == 'Joe'
        assert user.last_name == 'Smith'
        assert user.has_course('CS111', 'CS151')
        assert user.has_skill('JAVA', 'HTML')

    def test_user_update(self, app, user):
        runner = app.test_cli_runner()
        options = ['-p', 'new_password', '-f', 'new_f', '-l', 'new_l', '-s', 'HTML', '-c', 'CS111']
        response = runner.invoke(commands.update_user, [user.email] + options)
        user.save()
        assert not response.exception
        assert user.check_password('new_password')
        assert user.first_name == 'new_f'
        assert user.last_name == 'new_l'
        assert user.has_course('CS111')
        assert user.has_skill('HTML')


    def test_user_activate(self, app, user):
        runner = app.test_cli_runner()
        assert user.active is False
        result = runner.invoke(commands.activate_user, [user.email])
        user.save()
        assert not result.exception
        assert user.active is True

    def test_user_deactivate(self, app, user):
        runner = app.test_cli_runner()
        user.update(active=True)
        assert user.active
        result = runner.invoke(commands.activate_user, [user.email, '-d'])
        user.save()
        assert not result.exception
        assert not user.active

    def test_user_query(self, app, user):
        runner = app.test_cli_runner()
        result = runner.invoke(commands.query_user, [user.email])
        assert not result.exception
        assert 'User does not exist' not in result.output
        assert user.email in result.output

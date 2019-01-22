from PEC import commands
from PEC.user.models import User


class TestUserGroup:

    def test_user_create(self, app, db):
        runner = app.test_cli_runner()
        assert User.query.filter_by(email='test@testing.com').first() is None
        result = runner.invoke(commands.create_user, input='y\ntest@testing.com\npass123\nJoe\nSmith\n')
        assert not result.exception
        user = User.query.filter_by(email='test@testing.com').first()
        assert user is not None
        assert user.email == 'test@testing.com'
        assert user.check_password('pass123')
        assert user.first_name == 'Joe'
        assert user.last_name == 'Smith'

    def test_user_activate(self, app, db, user):
        runner = app.test_cli_runner()
        assert user.active is False
        result = runner.invoke(commands.activate_user, [user.email])
        db.session.add(user)
        db.session.commit()
        assert not result.exception
        assert user.active is True

    def test_user_query(self, app, db, user):
        runner = app.test_cli_runner()
        result = runner.invoke(commands.query_user, [user.email])
        assert not result.exception
        assert 'User does not exist' not in result.output
        assert user.email in result.output

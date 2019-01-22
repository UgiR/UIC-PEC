from flask_login import login_user
from tests.factories import UserFactory
from PEC.settings.forms import AccountDetailForm


class TestAccountDetailForm:

    def test_valid(self, user):
        login_user(user)
        form = AccountDetailForm()
        form.first_name.data = 'Other'
        form.last_name.data = 'Name'
        form.email.data = user.email
        assert form.validate() is True

    def test_duplicate_email(self, user):
        login_user(user)
        user2 = UserFactory()
        form = AccountDetailForm()
        form.first_name.data = 'Other'
        form.last_name.data = 'Name'
        form.email.data = user2.email
        assert form.validate() is False

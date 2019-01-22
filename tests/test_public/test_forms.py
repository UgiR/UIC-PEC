from flask_login import login_user
from tests.factories import UserFactory
from PEC.public.forms import LoginForm, RegisterForm
from PEC.settings.forms import AccountDetailForm


class TestLoginForm:

    def test_empty_input(self, app):
        form = LoginForm()
        assert form.validate() is False
        form.email.data = ''
        form.password.data = ''
        assert form.validate() is False

    def test_valid_not_active(self, user):
        form = LoginForm()
        form.email.data = user.email
        form.password.data = 'password'
        assert user.check_password('password') is True
        assert form.validate() is False

    def test_valid(self, user):
        form = LoginForm()
        form.email.data = user.email
        form.password.data = 'password'
        user.active = True
        user.save()
        assert form.validate() is True
        assert form.user is user

    def test_invalid(self, user):
        form = LoginForm()
        form.email.data = user.email
        form.password.data = 'password' + '1'
        user.active = True
        user.save()
        assert form.validate() is False
        assert len(form.password.errors) > 0


class TestRegisterForm:

    def test_email_exists(self, db, user):
        form = RegisterForm()
        form.email.data = user.email
        form.password.data = 'some_password'
        form.password_confirm.data = 'some_password'
        assert form.validate() is False
        assert len(form.email.errors) > 0

    def test_password_mismatch(self, db):
        form = RegisterForm()
        form.email.data = 'user@mail.com'
        form.password.data = 'some_password'
        form.password_confirm.data = 'Some_password'
        assert form.validate() is False
        assert len(form.password_confirm.errors) > 0

    def test_valid_form(self, db):
        form = RegisterForm()
        form.email.data = 'user@mail.com'
        form.password.data = 'password'
        form.password_confirm.data = 'password'
        assert form.validate() is True
from flask import url_for
from tests.utils import login_request


class TestWebPublic:

    def test_home(self, webapp):
        response = webapp.get(url_for('public.index'))
        assert response.status_code == 200
        assert 'Sign in/Register' in response.text

    def test_login(self, webapp, user):
        user.update(active=True)
        response = webapp.get(url_for('public.login'))
        form = response.forms['loginForm']
        form['email'] = user.email
        form['password'] = 'password'
        response = form.submit().maybe_follow()
        assert 'loginForm' not in response.forms
        assert response.status_code == 200

    def test_login_next(self, webapp, user):
        user.update(active=True)
        response = webapp.get(url_for('public.login', next=url_for('user.profile', user_id=user.uuid)))
        form = response.forms['loginForm']
        form['email'] = user.email
        form['password'] = 'password'
        response = form.submit().follow()
        assert 'loginForm' not in response.forms
        assert response.status_code == 200
        assert str(user.uuid) in response.request.url

    def test_register(self, webapp):
        response = webapp.get(url_for('public.register'))
        assert response.status_code == 200
        assert 'registerForm' in response.forms


class TestWebSettings:

    def test_login_required(self, webapp):
        app = webapp.app
        for rule in app.url_map.iter_rules():
            if 'settings' in rule.endpoint and 'static' not in rule.endpoint:
                response = webapp.get(url_for(rule.endpoint), expect_errors=True)
                assert response.status_code == 401

    def test_account_details(self, webapp, user):
        user.update(active=True)
        login_request(user, 'password', webapp)
        response = webapp.get(url_for('settings.account_details'), expect_errors=True)
        assert response.status_code == 200
        assert 'detailsForm' in response.forms

    def test_account_portfolio(self, webapp, user):
        user.update(active=True)
        login_request(user, 'password', webapp)
        response = webapp.get(url_for('settings.account_portfolio'), expect_errors=True)
        assert response.status_code == 200
        assert 'portfolioForm' in response.forms

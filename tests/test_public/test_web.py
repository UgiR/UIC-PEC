import pytest
from flask import url_for


@pytest.mark.usefixtures('db')
class TestEndpoints:

    def test_returns_ok(self, webapp):
        '''Tests that all public endpoints return 200'''
        exclusions = ['static', 'logout']
        app = webapp.app
        rules = [r for r in app.url_map.iter_rules() if r.endpoint.split('.')[0] == 'public']
        endpoints = [r.endpoint for r in rules if r.endpoint.split('.')[1] not in exclusions]
        for endpoint in endpoints:
            response = webapp.get(url_for(endpoint), expect_errors=True)
            print('{}: {}'.format(endpoint, response.status_code))
            assert response.status_code == 200


@pytest.mark.usefixtures('db')
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

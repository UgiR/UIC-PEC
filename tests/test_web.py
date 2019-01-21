import pytest
from flask import url_for
from tests.utils import login_request
from PEC.user.models import User
from PEC.user.attributes import Skill, Course


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


@pytest.mark.usefixtures('db')
class TestWebSettings:

    def test_login_required(self, webapp):
        '''Tests that all settings endpoints return 401 when not logged in'''
        app = webapp.app
        for rule in app.url_map.iter_rules():
            if 'settings' in rule.endpoint and 'static' not in rule.endpoint:
                response = webapp.get(url_for(rule.endpoint), expect_errors=True)
                assert response.status_code == 401

    def test_account_details(self, webapp, user):
        '''Tests account_details endpoint returns 200, contains the form, and form successfully updates user'''
        user.update(active=True)
        login_request(user, 'password', webapp)
        response = webapp.get(url_for('settings.account_details'))
        assert response.status_code == 200
        assert 'detailsForm' in response.forms
        form = response.forms['detailsForm']
        form['first_name'] = 'test_name_z'
        form['last_name'] = 'test_last_z'
        form['email'] = 'new@new.com'
        form.submit()
        u = User.query.get(user.id)
        assert u.first_name == 'test_name_z'
        assert u.last_name == 'test_last_z'
        assert u.email == 'new@new.com'

    def test_account_github(self, webapp, user):
        user.update(active=True)
        login_request(user, 'password', webapp)
        response = webapp.get(url_for('settings.account_github_auth')).follow(expect_errors=True)
        assert 'github.com/login/oauth/authorize' in response.request.url

    def test_account_portfolio(self, webapp, user):
        '''Tests account_portfolio endpoint returns 200, contains the form, and form successfully updates user'''
        user.update(active=True)
        login_request(user, 'password', webapp)
        response = webapp.get(url_for('settings.account_portfolio'))
        assert response.status_code == 200
        assert 'portfolioForm' in response.forms
        form = response.forms['portfolioForm']
        form['skill_selection'] = ['React', 'Flask']
        form['course_selection'] = ['Program Design I', 'Program Design II']
        form.submit()
        u = User.query.get(user.id)
        assert u.has_skill(Skill('React'))
        assert u.has_skill(Skill('Flask'))
        assert u.has_course(Course('Program Design I'), Course('Program Design II'))

import pytest
from flask import url_for
from tests.utils import login_request
from PEC.user.models import User
from PEC.user.attributes import Skill as Skill_
from PEC.user.attributes import Course as Course_


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
        assert u.has_skill(Skill_('React'))
        assert u.has_skill(Skill_('Flask'))
        assert u.has_course(Course_('Program Design I'), Course_('Program Design II'))

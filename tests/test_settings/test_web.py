import pytest
from flask import url_for, session
from tests.utils import login_request
from PEC.user.models import User


@pytest.mark.usefixtures('db')
class TestEndpoints:

    def test_login_required(self, webapp):
        '''Tests that all settings endpoints return 401 when not logged in'''
        exclusions = ['static']
        app = webapp.app
        rules = [r for r in app.url_map.iter_rules() if r.endpoint.split('.')[0] == 'settings']
        endpoints = [r.endpoint for r in rules if r.endpoint.split('.')[1] not in exclusions]
        for endpoint in endpoints:
            if 'settings' in endpoint and 'static' not in endpoint:
                response = webapp.get(url_for(endpoint), expect_errors=True)
                assert response.status_code == 401

    def test_returns_ok(self, webapp, user):
        '''Tests that all settings endpoints return 200 when logged in'''
        exclusions = ['static', 'account_github_auth', 'account_github_auth_callback']
        login_request(user, 'password', webapp)
        app = webapp.app
        rules = [r for r in app.url_map.iter_rules() if r.endpoint.split('.')[0] == 'settings']
        endpoints = [r.endpoint for r in rules if r.endpoint.split('.')[1] not in exclusions]
        for endpoint in endpoints:
            response = webapp.get(url_for(endpoint), expect_errors=True)
            print('{}: {}'.format(endpoint, response.status_code))
            assert response.status_code == 200


@pytest.mark.usefixtures('db')
class TestAccountDetails:

    def test_form_present(self, webapp, user):
        '''Tests account_details endpoint returns 200, contains the form'''
        login_request(user, 'password', webapp)
        response = webapp.get(url_for('settings.account_details'))
        assert response.status_code == 200
        assert 'detailsForm' in response.forms

    def test_form_functional(self, webapp, user):
        '''Tests account_details form successfully updates user'''
        login_request(user, 'password', webapp)
        response = webapp.get(url_for('settings.account_details'))
        form = response.forms['detailsForm']
        form['first_name'] = 'test_name_z'
        form['last_name'] = 'test_last_z'
        form['email'] = 'new@new.com'
        form.submit()
        u = User.query.get(user.id)
        assert u.first_name == 'test_name_z'
        assert u.last_name == 'test_last_z'
        assert u.email == 'new@new.com'


@pytest.mark.usefixtures('db')
class TestAccountPortfolio:

    def test_form_present(self, webapp, user):
        '''Tests account_portfolio endpoint returns 200, contains the form'''
        login_request(user, 'password', webapp)
        response = webapp.get(url_for('settings.account_portfolio'))
        assert response.status_code == 200
        assert 'portfolioForm' in response.forms

    def test_account_portfolio(self, webapp, user):
        '''Tests account_portfolio form successfully updates user'''
        login_request(user, 'password', webapp)
        response = webapp.get(url_for('settings.account_portfolio'))
        form = response.forms['portfolioForm']
        form['skill_selection'] = ['REACT', 'FLASK']
        form['course_selection'] = ['CS111', 'CS141']
        form.submit()
        u = User.query.get(user.id)
        assert u.has_skill('REACT')
        assert u.has_skill('FLASK')
        assert u.has_course('CS111', 'CS141')


@pytest.mark.usefixtures('db')
class TestAccountGithubAuth:

    def test_github_redirect(self, webapp, user):
        '''Github auth redirects to github'''
        login_request(user, 'password', webapp)
        response = webapp.get(url_for('settings.account_github_auth')).follow(expect_errors=True)
        assert 'github.com/login/oauth/authorize' in response.request.url

    def test_github_state_stored(self, webapp, user):
        '''Github state stored in session on auth'''
        with webapp.app.test_client() as c:
            assert session.get('github_state') is None
            login_request(user, 'password', c)
            c.get(url_for('settings.account_github_auth'))
            assert session.get('github_state') is not None

    def test_github_state_removed(self, webapp, user):
        '''Github state removed from session on callback'''
        with webapp.app.test_client() as c:
            assert session.get('github_state') is None
            login_request(user, 'password', c)
            c.get(url_for('settings.account_github_auth'))
            assert session.get('github_state') is not None
            c.get(url_for('settings.account_github_auth_callback'))
            assert session.get('github_state') is None

    def test_github_already_linked(self, webapp, user):
        '''Account redirects to settings page if Github already linked and auth attempted'''
        user.update(github_id=1)  # not null
        login_request(user, 'password', webapp)
        response = webapp.get(url_for('settings.account_github_auth')).follow(expect_errors=True)
        assert url_for('settings.account_details') in response.request.url

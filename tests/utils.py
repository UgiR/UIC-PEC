from flask.testing import FlaskClient
from webtest.app import TestApp


def login_request(user, password, a):
    user.update(active=True)
    if isinstance(a, TestApp):
        return a.post_json('/login', dict(
                    email=user.email,
                    password=password
                ))
    elif isinstance(a, FlaskClient):
        return a.post('/login', data=dict(
            email=user.email,
            password=password
        ),  follow_redirects=True)

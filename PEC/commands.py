import os
import click
from flask.cli import AppGroup

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')
TEST_PATH_USER = os.path.join(PROJECT_ROOT, 'tests/test_user')

user_cli = AppGroup('user')
test_cli = AppGroup('test')


@test_cli.command()
@click.argument('target', required=False)
def test(target):
    import pytest
    if target == 'all' or target is None:
        rv = pytest.main([TEST_PATH, '--verbose'])
    else:
        test_dir = os.path.join(PROJECT_ROOT, 'tests/test_{}'.format(target))
        rv = pytest.main([test_dir, '--verbose'])
    exit(rv)


@user_cli.command('query')
@click.argument('email')
def query_user(email):
    """Fetches registered user by e-mail"""
    from PEC.user.models import User
    user = User.query.filter_by(email=email).first()
    if user is None:
        click.echo('User does not exist')
    else:
        click.echo(user.uuid)
        click.echo(user.email)
        click.echo(user.first_name)
        click.echo(user.last_name)


# TODO: allow prompts to be supplied as arguments
@user_cli.command('create')
def create_user():
    """Creates new user in database"""
    click.echo('All user registration should be completed through the Register form.')
    click.confirm('Continue?', abort=True)
    from PEC.user.models import User
    email = click.prompt('Email', type=str)
    password = click.prompt('Password', type=str)
    first_name = click.prompt('First name', type=str, default='')
    last_name = click.prompt('Last name', type=str, default='')
    user = User(email, password)
    user.first_name = first_name
    user.last_name = last_name
    if user.validate():
        user.save()
    else:
        click.echo('Unable to create user')


@user_cli.command('activate')
@click.argument('email')
def activate_user(email):
    """Activates user account"""
    from PEC.user.models import User
    user = User.query.filter_by(email=email).first()
    if user is not None:
        if not user.active:
            user.update(active=True)
            click.echo('User activated')
        else:
            click.echo('User already active')
    else:
        click.echo('User not found')

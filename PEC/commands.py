import os
import click
from flask.cli import AppGroup

HERE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(HERE, os.pardir)
TEST_PATH = os.path.join(PROJECT_ROOT, 'tests')

user_cli = AppGroup('user')
project_cli = AppGroup('project')
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


# TODO: Implement --full option, and other options
@user_cli.command('query')
@click.argument('email')
@click.option('--full', is_flag=True)
def query_user(email, full):
    """Fetches registered user by e-mail"""
    from PEC.user.models import User
    user = User.query.filter_by(email=email).first()
    if user is None:
        click.echo('User does not exist')
    else:
        click.echo('UUID: {}'.format(user.uuid))
        click.echo('EMAIL: {}'.format(user.email))
        click.echo('FIRST: {}'.format(user.first_name))
        click.echo('LAST: {}'.format(user.last_name))


@user_cli.command('create')
@click.argument('email')
@click.option('--password', '-p', prompt=True, hide_input=True, confirmation_prompt=True)
@click.option('--first_name', '-f', default=None)
@click.option('--last_name', '-l', default=None)
@click.option('--skill', '-s', multiple=True)
@click.option('--course', '-c', multiple=True)
def create_user(email, password, first_name, last_name, skill, course):
    """Creates new user in database"""
    from PEC.user.models import User
    if not User.exists(email=email):
        user = User(email, password)
        try:
            user.first_name = first_name
            user.last_name = last_name
            user.add_skill(* skill)
            user.add_course(* course)
            user.save()
        except KeyError as e:
            click.echo('Invalid attribute {}'.format(e))
    else:
        click.echo('Unable to create user')


@user_cli.command('update')
@click.argument('email')
@click.option('--password', '-p')
@click.option('--first_name', '-f')
@click.option('--last_name', '-l')
@click.option('--skill', '-s')
@click.option('--course', '-c')
def update_user(email, password, first_name, last_name, skill, course):
    """Updates existing user. (Updating skills/courses will reset current options)"""
    from PEC.user.models import User
    user = User.query.filter_by(email=email).first()
    if user is not None:
        if password:
            user.set_password(password)
        if first_name:
            user.update(first_name=first_name, commit=False)
        if last_name:
            user.update(last_name=last_name, commit=False)
        if skill:
            print(skill)
            user.skills.clear()
            user.add_skill(*skill)
        if course:
            user.courses.clear()
            user.add_course(*course)
        user.save()
    else:
        click.echo('User does not exist')


@user_cli.command('activate')
@click.argument('email')
@click.option('--disable', '-d', is_flag=True)
def activate_user(email, disable):
    """Activates user account"""
    from PEC.user.models import User
    user = User.query.filter_by(email=email).first()
    if user is not None:
        if disable and not user.active:
            click.echo('User already inactive')
        elif disable:
            user.update(active=False)
        elif not user.active:
            user.update(active=True)
            click.echo('User activated')
        else:
            click.echo('User already active')
    else:
        click.echo('User not found')


@project_cli.command('create')
@click.option('--email', '-e', required=True, prompt=True)
@click.option('--title', '-t', required=True, prompt=True)
@click.option('--description', '-d', default='')
def create_project(email, title, description):
    """Creates new project in database"""
    from PEC.project.models import Project
    from PEC.user.models import User
    user = User.query.filter_by(email=email).first()
    if user is None:
        click.echo('User not found')
    else:
        project = Project()
        project.title = title
        project.description = description
        project.mark_development(commit=False)
        user.projects.append(project)
        user.save()

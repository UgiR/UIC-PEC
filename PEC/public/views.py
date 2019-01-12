import datetime as dt
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from PEC.utils import flash_form_errors
from .forms import LoginForm, RegisterForm

blueprint = Blueprint('public', __name__, static_folder='../static')


@blueprint.route('/')
def index():
    """ Main home page
    """
    return render_template('public/index.html')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """ Login page
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            login_user(login_form.user, remember=login_form.remember_me.data)
            login_form.user.update(last_login_at=dt.datetime.utcnow())
            next_page = request.args.get('next') or url_for('public.index')
            return redirect(next_page)
        else:
            flash_form_errors(login_form)
    return render_template('public/login.html', login_user_form=login_form)


@blueprint.route('/logout')
def logout():
    """ Logout endpoint
    """
    logout_user()
    return redirect(url_for('public.index'))


@blueprint.route('/register')
def register():
    """ User registration page
    """
    register_form = RegisterForm()
    return render_template('public/register.html', register_form=register_form)

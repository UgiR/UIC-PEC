from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from .forms import LoginForm

blueprint = Blueprint('public', __name__, static_folder='../static')


@blueprint.route('/')
def index():
    return render_template('public/index.html')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    login_form = LoginForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            login_user(login_form.user, remember=login_form.remember_me.data)
            next_page = request.args.get('next') or url_for('public.index')
            return redirect(next_page)
        else:
            flash(login_form.errors)
    return render_template('public/login.html', login_user_form=login_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))

@blueprint.route('/props')
def test():
    return render_template('public/all_proposals.html')
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, current_app
from flask_login import current_user, login_required
from werkzeug import security
import requests
from github import Github
from PEC.settings.forms import AccountDetailForm, PortfolioForm, UpdatePasswordForm
from PEC.user.models import User
from PEC.utils import flash_form_errors

blueprint = Blueprint('settings', __name__, static_folder='../static', url_prefix='/settings')


@blueprint.route('/account/details', methods=['GET', 'POST'])
@login_required
def account_details():
    """ Account details settings page
    """
    detail_form = AccountDetailForm()
    password_form = UpdatePasswordForm()
    if request.method == 'POST':
        if detail_form.validate_on_submit():
            current_user.update(first_name=detail_form.first_name.data, last_name=detail_form.last_name.data,
                                email=detail_form.email.data)
            flash('Account details updated')
        elif password_form.validate_on_submit():
            current_user.set_password(password_form.new_password.data)
        else:
            flash_form_errors(detail_form)
            flash_form_errors(password_form)
        return redirect(url_for('settings.account_details'))
    return render_template('settings/account-settings.html',
                           detail_form=detail_form,
                           password_form=password_form)


@blueprint.route('/account/github/auth')
@login_required
def account_github_auth():
    if current_user.github_id is not None:
        flash('GitHub email already set')
        return redirect(url_for('settings.account_details'))
    state = security.gen_salt(10)
    session['github_state'] = state
    url = 'https://github.com/login/oauth/authorize?scope=user:email&client_id={}&state={}'
    return redirect(url.format(current_app.config['GITHUB_CLIENT_ID'], state))


@blueprint.route('/account/github/auth/callback')
@login_required
def account_github_auth_callback():
    state = session.get('github_state')
    if state is None:
        flash('Error in authorization process. Try again.')
        return redirect(url_for('settings.account_details'))
    session.pop('github_state')
    received_code = request.args.get('code')
    received_state = request.args.get('state')
    if received_state != state:
        flash('Error in authorization process. Try again.')
        return redirect(url_for('settings.account_details'))
    data = {
        'client_id': current_app.config['GITHUB_CLIENT_ID'],
        'client_secret': current_app.config['GITHUB_CLIENT_SECRET'],
        'code': received_code,
        'state': state
    }
    res = requests.post('https://github.com/login/oauth/access_token', data=data, headers={'Accept': 'application/json'})
    gh = Github(res.json()['access_token'])
    gh_id = gh.get_user().id
    u = User.query.filter_by(github_id=gh_id).first()
    if u is not None:
        flash('GitHub account already associated with a user')
        return redirect(url_for('settings.account_details'))
    current_user.update(github_id=gh_id)
    return redirect(url_for('settings.account_details'))


@blueprint.route('/account/portfolio', methods=['GET', 'POST'])
@login_required
def account_portfolio():
    """ Account portfolio settings page
    """
    current_courses = [c.name.value for c in current_user.courses]
    current_skills = [s.name.value for s in current_user.skills]
    portfolio_form = PortfolioForm(course_selection=current_courses, skill_selection=current_skills)

    if request.method == 'POST':
        if portfolio_form.validate_on_submit():
            current_user.courses.clear()
            current_user.add_skill(*portfolio_form.skill_selection.data)
            current_user.add_course(*portfolio_form.course_selection.data)
            current_user.save()
            return redirect(url_for('settings.account_portfolio'))
        else:
            flash_form_errors(portfolio_form)
            return redirect(url_for('settings.account_portfolio'))
    return render_template('settings/account/portfolio.html', portfolio_form=portfolio_form)

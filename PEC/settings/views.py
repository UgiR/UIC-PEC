from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from PEC.settings.forms import AccountDetailForm, PortfolioForm
from PEC.user.attributes import Course, Skill
from PEC.user.models import Course as Course_
from PEC.user.models import Skill as Skill_
from PEC.utils import flash_form_errors

blueprint = Blueprint('settings', __name__, static_folder='../static', url_prefix='/settings')


@blueprint.route('/account/details', methods=['GET', 'POST'])
@login_required
def account_details():
    """ Account details settings page
    """
    detail_form = AccountDetailForm()
    if request.method == 'POST':
        if detail_form.validate_on_submit():
            current_user.update(first_name=detail_form.first_name.data, last_name=detail_form.last_name.data,
                                email=detail_form.email.data)
            flash('Account details updated')
            return redirect(url_for('settings.account_details'))
        else:
            flash_form_errors(detail_form)
            return redirect(url_for('settings.account_details'))
    return render_template('settings/account/details.html', uuid=current_user.uuid, detail_form=detail_form)


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
            for selected in portfolio_form.course_selection.data:
                course = Course_.get(name=Course(selected))
                current_user.courses.append(course)
            for selected in portfolio_form.skill_selection.data:
                skill = Skill_.get(name=Skill(selected))
                current_user.skills.append(skill)
            current_user.save()
            return redirect(url_for('settings.account_portfolio'))
        else:
            flash_form_errors(portfolio_form)
            return redirect(url_for('settings.account_portfolio'))

    return render_template('settings/account/portfolio.html', portfolio_form=portfolio_form)
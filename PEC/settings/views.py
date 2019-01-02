from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from PEC.settings.forms import AccountDetailForm

blueprint = Blueprint('settings', __name__, static_folder='../static', url_prefix='/settings')


@blueprint.route('/account/details', methods=['GET', 'POST'])
@login_required
def account_details():
    detail_form = AccountDetailForm()
    if request.method == 'POST':
        if detail_form.validate_on_submit():
            current_user.update(first_name=detail_form.first_name.data, last_name=detail_form.last_name.data,
                                email=detail_form.email.data)
            flash('Account details updated')
            return redirect(url_for('settings.account_details'))
        else:
            flash(detail_form.errors)
            return redirect(url_for('settings.account_details'))
    return render_template('settings/account/details.html', uuid=current_user.uuid, detail_form=detail_form)

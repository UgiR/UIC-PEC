from flask import Blueprint, render_template
from PEC.user.models import User

blueprint = Blueprint('user', __name__, static_folder='../static', url_prefix='/user')


@blueprint.route('/<user_id>')
def user(user_id):
    _user = User.query.filter_by(uuid=user_id).first()
    return render_template('user/user.html', user=_user)

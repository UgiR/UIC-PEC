from flask import Blueprint

blueprint = Blueprint('projects', __name__, static_folder='../static', url_prefix='/project')


@blueprint.route('/<project_id>')
def project(project_id):
    pass

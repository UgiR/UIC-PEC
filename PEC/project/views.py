from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from PEC.project.models import Project
from PEC.utils import flash_form_errors
from .forms import NewProjectForm
from .attributes import Status

blueprint = Blueprint('project', __name__, static_folder='../static', url_prefix='/project')


@blueprint.route('/<project_id>')
def project(project_id):
    """ TODO: Page to display specific project

    :param project_id: Project uuid
    """
    project_ = Project.query.filter_by(uuid=project_id).first()
    return render_template('project/project.html', project=project_)


@blueprint.route('/showcase')
def showcase():
    """ TODO: Page to display all projects
    """
    projects = Project.query.all()
    return render_template('project/showcase.html', projects=projects)


@blueprint.route('/new', methods=['GET', 'POST'])
def new():
    """ Page/form to create/submit a new project
    """
    project_form = NewProjectForm()
    if request.method == 'POST':
        if project_form.validate_on_submit():
            project_ = Project.from_project_form(project_form)
            project_.status = Status.development
            current_user.projects.append(project_)
            project_.contributors.append(current_user)
            project_.save()
            current_user.save()
            return redirect(url_for('project.project', project_id=project_.uuid))
        else:
            flash_form_errors(project_form)

    return render_template('project/new_project.html', project_form=project_form)

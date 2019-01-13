from flask import Flask
from PEC import public, user, settings, project, commands
from PEC.user.models import User, Role
from PEC.project.models import Project
from PEC.extensions import db, migrate, login_manager, principal


def create_app(config_object='PEC.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_shell_context(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    principal.init_app(app)


def register_blueprints(app):
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(settings.views.blueprint)
    app.register_blueprint(project.views.blueprint)


def register_commands(app):
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.user_cli)


def register_shell_context(app):
    def shell_context():
        return {
            'db': db,
            'User': User,
            'Role': Role,
            'Project': Project
        }
    app.shell_context_processor(shell_context)

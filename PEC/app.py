from flask import Flask
from PEC import public, commands
from PEC.extensions import db, migrate, login_manager, principal


def create_app(config_object='PEC.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)
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


def register_commands(app):
    app.cli.add_command(commands.test)
    app.cli.add_command(commands.user_cli)

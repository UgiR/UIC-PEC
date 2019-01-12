from flask import flash


def flash_form_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0}: {1}'.format(field, error))

from flask import flash


def flash_form_errors(form):
    """ Flashes all form errors individually

    :param form: WTF form
    :return:
    """
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0}: {1}'.format(field, error))

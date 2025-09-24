from flask import abort, current_app, render_template

from app.lib.errors import DataAccessError

from . import bp
from .service import get_about_info


@bp.route('/')
def about():
    try:
        about_info = get_about_info()
    except DataAccessError:
        current_app.logger.exception("Failed to load about page")
        abort(500)
    if not about_info:
        abort(404)
    return render_template('about.html', about_info=about_info)

from flask import abort, current_app, render_template

from . import about_bp
from app.lib.errors import DataAccessError
from app.services import about_service


@about_bp.route('/')
def about():
    try:
        about_info = about_service.get_about_info()
    except DataAccessError:
        current_app.logger.exception("Failed to load about page")
        abort(500)
    if not about_info:
        abort(404)
    return render_template('about.html', about_info=about_info)

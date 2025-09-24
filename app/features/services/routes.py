from flask import abort, current_app, render_template

from app.lib.errors import DataAccessError

from . import bp
from .service import get_services


@bp.route('/')
def services_list():
    try:
        services = get_services()
    except DataAccessError:
        current_app.logger.exception("Failed to load services list")
        abort(500)
    return render_template('services.html', services=services)

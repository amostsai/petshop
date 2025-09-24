from flask import abort, current_app, render_template

from . import services_bp
from app.lib.errors import DataAccessError
from app.services import services_service


@services_bp.route('/')
def services_list():
    try:
        services = services_service.get_services()
    except DataAccessError:
        current_app.logger.exception("Failed to load services list")
        abort(500)
    return render_template('services.html', services=services)

from flask import abort, current_app, render_template

from app.features.news.service import get_latest_news
from app.features.services.service import get_services
from app.lib.errors import DataAccessError

from . import bp


@bp.route('/')
def index():
    try:
        news = get_latest_news(limit=3)
        services = get_services(limit=4)
    except DataAccessError:
        current_app.logger.exception("Failed to load homepage data")
        abort(500)
    return render_template('index.html', news=news, services=services)

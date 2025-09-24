from flask import abort, current_app, render_template

from app.lib.errors import DataAccessError

from . import bp
from .service import get_news_detail, get_news_list


@bp.route('/')
def news_list():
    try:
        news = get_news_list()
    except DataAccessError:
        current_app.logger.exception("Failed to load news list")
        abort(500)
    return render_template('news.html', news=news)


@bp.route('/<int:news_id>')
def news_detail(news_id):
    try:
        news = get_news_detail(news_id)
    except DataAccessError:
        current_app.logger.exception("Failed to load news detail")
        abort(500)
    if not news:
        abort(404)
    return render_template('news_detail.html', news=news)

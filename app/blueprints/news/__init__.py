from flask import Blueprint

news_bp = Blueprint('news', __name__)

from . import routes

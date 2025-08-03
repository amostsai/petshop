from flask import Blueprint

about_bp = Blueprint('about', __name__)

from . import routes

from flask import Blueprint

bp = Blueprint('about', __name__, template_folder='templates')

from . import routes  # noqa: E402, F401

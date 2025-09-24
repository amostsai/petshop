from flask import Flask

from .blueprints import register_blueprints
from .config import get_config
from .lib.db import init_app as init_db


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    config_class = get_config(config_name)
    app.config.from_object(config_class)

    register_blueprints(app)
    init_db(app)

    return app


app = create_app()

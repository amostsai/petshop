from flask import Flask

from .features import register_features
from .config import get_config
from .lib.db import init_app as init_db


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)
    config_class = get_config(config_name)
    app.config.from_object(config_class)

    register_features(app)
    init_db(app)

    @app.context_processor
    def inject_cart_badge():
        try:
            from app.lib import cart as cart_utils

            summary = cart_utils.summarize()
            return {
                'cart_item_count': summary['total_quantity'],
            }
        except Exception:
            return {'cart_item_count': 0}

    return app


app = create_app()

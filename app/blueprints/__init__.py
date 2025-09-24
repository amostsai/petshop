from .about import about_bp
from .main import main_bp
from .news import news_bp
from .services import services_bp


def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(news_bp, url_prefix='/news')
    app.register_blueprint(services_bp, url_prefix='/services')
    app.register_blueprint(about_bp, url_prefix='/about')

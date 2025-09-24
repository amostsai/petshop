from . import about, contact, main, news, services


def register_features(app):
    app.register_blueprint(main.bp)
    app.register_blueprint(news.bp, url_prefix='/news')
    app.register_blueprint(services.bp, url_prefix='/services')
    app.register_blueprint(about.bp, url_prefix='/about')
    app.register_blueprint(contact.bp, url_prefix='/contact')

import os

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
    )
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from data import db
    db.init_app(app)

    from data import application_user, application_tests
    app.register_blueprint(application_user.bp)
    app.register_blueprint(application_tests.bp)

    return app

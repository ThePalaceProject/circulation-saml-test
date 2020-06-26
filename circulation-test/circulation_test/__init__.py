import logging
import os

from flask import Flask

from circulation_test.blueprints import home, auth, books


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    logging.basicConfig(level=logging.INFO)

    app.config.from_object('circulation_test.config.Config')

    if os.getenv('APPLICATION_SETTINGS'):
        app.config.from_envvar('APPLICATION_SETTINGS')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(auth.blueprint)
    app.register_blueprint(books.blueprint)
    app.register_blueprint(home.blueprint)

    return app

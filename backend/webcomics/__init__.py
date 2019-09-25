import os
import sys
from logging.config import dictConfig

from flask import Flask


# Configure logging
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'filename': os.path.join(os.path.expanduser('~'), 'webcomics', 'logs', 'app.log'),
            'maxBytes': 4096,
            'backupCount': 3
        },
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stderr,
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['file', 'console']
    }
})


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True, static_url_path='/webcomics/static')
    app.config.from_mapping(
        SECRET_KEY='dev_secret',
        DATABASE=os.path.join(app.instance_path, "webcomics.sqlite")
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # TODO: handle this better
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp, url_prefix="/webcomics")

    from . import comics
    app.register_blueprint(comics.bp, url_prefix="/webcomics")
    app.add_url_rule("/webcomics", endpoint="index")

    app.logger.info('Application created.')
    return app

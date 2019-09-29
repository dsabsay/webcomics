import os
import sys
from logging.config import dictConfig

from flask import Flask


def init_logging(app):
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
                'filename': os.path.join(app.instance_path, 'app.log'),
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


def config_is_valid(config):
    '''
    Returns True if config has necessary keys, False otherwise.
    '''
    required = [
        'DATABASE',
        'DB_BACKUP_LOCAL_REPO',
        'DB_BACKUP_REMOTE_REPO',
        'DB_BACKUP_DEPLOY_KEY',
        'SECRET_KEY',
        'DB_BACKUP_INTERVAL',
        'DB_BACKUP_TIME_UNIT'
    ]

    return all(config.get(key, None) is not None for key in required)


def create_app(test_config=None):
    os.environ['SCRIPT_NAME'] = '/webcomics'
    app = Flask(__name__, instance_relative_config=True, static_url_path='/static')
    init_logging(app)

    if test_config is None:
        with app.app_context():  # Allow access to current_app in config.py
            app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    if not config_is_valid(app.config):
        app.logger.error('Invalid configuration. Exiting. Check that all required fields are set.')
        sys.exit(1)

    # TODO: handle this better
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import comics
    app.register_blueprint(comics.bp)
    app.add_url_rule('/', endpoint='index')
    # app.add_url_rule("/webcomics", endpoint="index")

    # Initialize CLI commands
    with app.app_context():
        # The jobs sub-package configures logging based on app.config
        from . import cli
    cli.init_cli(app)

    app.logger.info('Application created.')
    return app

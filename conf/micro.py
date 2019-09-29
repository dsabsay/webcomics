import os

from flask import current_app


_THIS_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(current_app.instance_path, 'db', 'webcomics.sqlite')
DB_BACKUP_LOCAL_REPO = os.path.join(current_app.instance_path, 'db_backup')
DB_BACKUP_REMOTE_REPO = 'git@github.com:dsabsay/webcomics-db-backup.git'
DB_BACKUP_DEPLOY_KEY = os.path.join(current_app.instance_path, 'db_backup_deploy_key_rsa')
DB_BACKUP_INTERVAL = 1
DB_BACKUP_TIME_UNIT = 'minutes'

SECRET_KEY = None
with open(os.path.join(_THIS_DIR, 'flask_secret_key')) as f:
    SECRET_KEY = f.read(-1)

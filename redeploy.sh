#! /bin/bash

set -e

# Kills existing gunicorn processes.
# Uninstalls webcomics from virtualenv
# Reinstalls webcomics from master branch
# Restarts gunicorn

if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo 'ERROR: Script must be run in the webcomics virtual environment'
    exit 1
fi

cd "${0%/*}"  # Change into directory of script

if [ -f 'gunicorn.pid' ]; then
    kill "$(cat gunicorn.pid)"
fi

pip uninstall webcomics
pip install --upgrade 'git+https://github.com/dsabsay/webcomics.git#egg=webcomics&subdirectory=app'

# Copy production configuration
cp conf/micro.py "${VIRTUAL_ENV}/var/webcomics-instance/config.py"

# Generate secret key for encrypting session data
flask_secret_key=$(python -c 'import os; print(os.urandom(16).hex())')

gunicorn --bind=127.0.0.1:4020 --workers=2 --daemon --pid=gunicorn.pid --env FLASK_SECRET_KEY="${flask_secret_key}" 'webcomics:create_app()'

echo 'Done.'

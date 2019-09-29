#! /bin/bash

set -e

# Kills existing gunicorn processes.
# Uninstalls webcomics from virtualenv
# Reinstalls webcomics from master branch
# Restarts gunicorn

cd "${0%/*}"  # Change into directory of script

if [ -f 'gunicorn.pid' ]; then
    kill "$(cat gunicorn.pid)"
fi

pip uninstall webcomics
pip install --upgrade 'git+https://github.com/dsabsay/webcomics.git#egg=webcomics&subdirectory=app'

# Copy production configuration
cp conf/micro.py "${VIRTUAL_ENV}/var/webcomics-instance/config.py"

gunicorn --bind=127.0.0.1:4020 --workers=2 --daemon --pid=gunicorn.pid 'webcomics:create_app()'

echo 'Done.'

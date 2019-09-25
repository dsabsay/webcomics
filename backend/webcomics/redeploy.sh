#! /bin/bash

set -e

# Kills existing gunicorn processes.
# Uninstalls webcomics from virtualenv
# Reinstalls webcomics from master branch
# Restarts gunicorn

pidfile='~/webcomics/gunicorn.pid'

cd "${0%/*}"  # Change into directory of script

if [ -f "$pidfile" ]; then
    echo '### Killing existing gunicorn processes...'
    kill "$(cat gunicorn.pid)"
fi

echo '### Uninstalling webcomics...'
pip uninstall --yes webcomics
echo '### Installing webcomics...'
pip install --upgrade 'git+https://github.com/dsabsay/webcomics.git#egg=webcomics&subdirectory=backend'

echo '### Starting gunicorn...'
gunicorn --bind=127.0.0.1:4020 --workers=2 --daemon --pid="$pidfile" 'webcomics:create_app()'

echo 'Done.'

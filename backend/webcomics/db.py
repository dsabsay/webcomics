import copy
import datetime
import os
import subprocess
import sqlite3

import click
import flask
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    close_db()


def run_shell_command(args, echo=False, env=None):
    '''
    Convenience wrapper around subprocess.run().

    Prints stdout and stderr of the subprocess to the parent's stdout and
    stderr. Checks return code, raising exception on non-zero exit code.
    '''
    cp = subprocess.run(args, check=False, capture_output=True, env=env)

    if echo:
        click.echo(cp.stdout)
        click.echo(cp.stderr, err=True)

    cp.check_returncode()


def backup_db(*, isManual):
    '''
    Performs the database backup, pushing to the configured repo
    on GitHub.

    Params:
        isManual (boolean) - True if invoked manually. False otherwise.
    '''
    local_repo = current_app.config['DB_BACKUP_LOCAL_REPO']
    backup_filename = 'webcomics_backup.sqlite'
    backup_path = os.path.join(
        local_repo,
        backup_filename
    )

    backup_db = sqlite3.connect(
        os.path.join(local_repo, backup_filename),
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    live_db = get_db()
    live_db.backup(backup_db, pages=0, name='main')
    close_db()  # closes the live db
    backup_db.close()

    cwd = os.getcwd()
    os.chdir(local_repo)
    run_shell_command(['git', 'add', backup_filename], echo=True)

    commit_time = datetime.datetime.now(tz=datetime.timezone.utc)
    commit_msg = f'{"Manual" if isManual else "Scheduled"} DB backup on {commit_time} UTC'
    run_shell_command(['git', 'commit', '-m', commit_msg], echo=True)

    deploy_key_path = current_app.config['DB_BACKUP_DEPLOY_KEY']
    env = copy.deepcopy(os.environ)
    env.update({ 'GIT_SSH_COMMAND': f'ssh -i {deploy_key_path}' })
    run_shell_command(['git', 'push', 'origin', 'master'], echo=True, env=env)

    os.chdir(cwd)


def init_app(app):
    """ Register DB functions with application instance. """
    # close db connection after response is returned
    app.teardown_appcontext(close_db)

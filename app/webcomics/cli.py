import click
import flask
from flask import current_app, g
from flask.cli import AppGroup

from webcomics.db import init_db, backup_db, get_db
from webcomics import jobs


@click.command('init-db')
@flask.cli.with_appcontext
def init_db_command():
    ''' Re-initializes the database. WARNING: This will delete any existing data! '''
    init_db()
    click.echo('Initialized the database.')


@click.command('backup-db')
@flask.cli.with_appcontext
def backup_db_command():
    '''
    Creates a backup of the database, writing it to a file in a Git
    repository, comitting it, and pushing the changes to the `origin`
    remote. The repository must already exist and the remote must be
    configured.

    This relies on the following configuration items:
        DB_BACKUP_LOCAL_REPO - path to local Git repository for backups
        DB_BACKUP_REMOTE_REPO - URL of remote repository for DB backups
        DB_BACKUP_DEPLOY_KEY - path to SSH deploy key for DB backup repo on GitHub
    '''
    backup_db(isManual=True)
    click.echo('Backup succeeded.')


@click.command('add-comic')
@flask.cli.with_appcontext
@click.argument('name')
@click.argument('author')
@click.argument('style')
@click.argument('link')
@click.option('--icon-url', type=str, help='URL to icon for comic.')
def add_comic_command(name, author, style, link, icon_url=None):
    '''
    Adds a new comic to the database.

    STYLE must be either "serial" or "episodic".
    '''
    if style not in ['serial', 'episodic']:
        click.echo('Invalid input. style must be either "serial" or "episodic".', err=True)
        sys.exit(1)

    db = get_db()
    db.execute(
        'INSERT INTO comics (name, author, link, iconUrl, style) VALUES (?, ?, ?, ?, ?)',
        (name, author, link, icon_url, style)
    )
    db.commit()
    click.echo(f'Added {name} to the database.')


@click.command('add-user')
@flask.cli.with_appcontext
@click.argument('username')
@click.argument('password')
def add_user_command(username, password):
    ''' Adds a new user to the database. '''
    db = get_db()
    db.execute(
        'INSERT INTO users (name, password) VALUES (?, ?)',
        (username, generate_password_hash(password))
    )
    db.commit()


webcomicsd_cli = AppGroup(
    'webcomicsd',
    help='''
    Interact with webcomicsd. webcomicsd is the worker process for background jobs.
    '''
)

@webcomicsd_cli.command('start')
@flask.cli.with_appcontext
def start_webcomicsd_command():
    '''
    Starts webcomicsd and saves its PID to <instance_path>/webcomics.pid
    '''
    jobs.start()


@webcomicsd_cli.command('stop')
@flask.cli.with_appcontext
def stop_webcomicsd_command():
    '''
    Kills the webcomicsd process.
    '''
    success = jobs.stop()
    if not success:
        click.echo('Kill signal sent, but process still alive.', err=True)
        sys.exit(1)

    click.echo('webcomicsd stopped.')


@webcomicsd_cli.command('status')
@flask.cli.with_appcontext
def status_webcomicsd_command():
    '''
    Checks the status of webcomicsd.
    '''
    msg = jobs.status()
    click.echo(msg)


def init_cli(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(backup_db_command)
    app.cli.add_command(add_user_command)
    app.cli.add_command(add_comic_command)
    app.cli.add_command(webcomicsd_cli)

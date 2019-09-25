import functools

import click
import flask
from flask import (
    Blueprint, redirect, g, render_template, flash, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from webcomics.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        user = db.execute(
            'SELECT * FROM users WHERE name = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


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


def init_app(app):
    ''' Register commands with application instance. '''
    app.cli.add_command(add_user_command)

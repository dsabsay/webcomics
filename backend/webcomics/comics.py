from flask import Blueprint, render_template, g, Response, request

from webcomics.db import get_db
from webcomics.auth import login_required


bp = Blueprint('comics', __name__)

@bp.route('/')
@login_required
def index():
    db = get_db()
    comics = db.execute(
        '''
        SELECT * FROM comics
        ORDER BY name ASC
        '''
    ).fetchall()
    comics = [dict(comic) for comic in comics]

    for comic in comics:
        comic['numUnread'] = get_num_unread(comic['name'])
        comic['bookmark'] = get_bookmark(comic['name']) if comic['style'] == 'serial' else None
        print(comic)

    return render_template('comics/index.html', comics=comics)


@bp.route('/strips/<string:comic_name>/')
@login_required
def strips(comic_name=None):
    db = get_db()
    strips = db.execute(
        '''
        SELECT stripsForComic.*, (stripId IS NOT NULL) as wasRead
        FROM (SELECT * FROM strips WHERE comic = ?) AS stripsForComic
        LEFT OUTER JOIN (SELECT * FROM reads WHERE userId = ?) AS userReads
        ON stripsForComic.id = userReads.stripId
        ORDER BY stripsForComic.datePublished DESC
        ''',
        (comic_name, g.user['id'])
    ).fetchall()
    strips = [dict(strip) for strip in strips]

    for strip in strips:
        strip['wasRead'] = bool(strip['wasRead'])

    comic = db.execute(
        '''
        SELECT * FROM comics WHERE name = ? LIMIT 1
        ''',
        (comic_name,)
    ).fetchone()
    comic = dict(comic)
    comic['bookmark'] = get_bookmark(comic_name)

    return render_template('comics/strips.html', strips=strips, comic=comic)


@bp.route('/bookmark', methods=['POST'])
@login_required
def bookmark():
    ''' Accepts a JSON payload with the URL to bookmark and saves the bookmark. '''
    # if request.content_type != 'application/json':
    #     resp = Response(status='Unsupported Media Type')
    #     resp.status_code = 415
    #     return resp

    bookmark_url = request.form['bookmark_url']
    comic_name = get_comic_name_from_url(bookmark_url)
    print(comic_name)

    db = get_db()
    existing = db.execute(
        'SELECT * FROM bookmarks WHERE comic = ?',
        (comic_name,)
    ).fetchone()

    result = None
    print(existing)
    if existing is None:
        result = db.execute(
            'INSERT INTO bookmarks VALUES (?, ?, ?)',
            (comic_name, g.user['id'], bookmark_url)
        )
        db.commit()
    else:
        result = db.execute(
            'UPDATE bookmarks SET link = ?  WHERE comic = ?',
            (bookmark_url, existing['comic'])
        )
        db.commit()

    return render_template('comics/bookmark.html', bookmark=result)


def get_comic_name_from_url(url):
    ''' Attempts to match the given URL to an existing comic in the DB. '''
    db = get_db()
    comics = db.execute(
        '''SELECT * FROM comics'''
    ).fetchall()

    for comic in comics:
        if comic['name'].lower() in url:
            return comic['name']

    return None


def get_num_unread(comic_name):
    ''' Computes the number of strips unread for `comic`. '''
    db = get_db()
    return db.execute(
        '''
        SELECT count(*) FROM (SELECT * FROM strips WHERE comic = ?) as stripsForComic
        LEFT OUTER JOIN (SELECT * FROM reads WHERE userId=?) AS userReads
        ON stripsForComic.id=userReads.stripId
        WHERE stripId IS NULL
        ''',
        (comic_name, g.user['id'])
    ).fetchone()['count(*)']


def get_bookmark(comic_name):
    ''' Returns the bookmark for the comic or None if no such bookmark exists. '''
    db = get_db()
    result = db.execute(
        '''
        SELECT link FROM bookmarks
        WHERE comic = ?
        LIMIT 1
        ''',
        (comic_name,)
    ).fetchone()

    if result is None:
        return None

    return result['link']

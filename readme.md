# webcomics

## Requirements
* Python 3.7 (because this uses `sqlite3.Connection.backup()`)
* On Ubuntu, the `python3.7-dev` package is required by `psutil`

## Deploying
To deploy the app, follow these steps:
1. Create a Python 3 virtual environment: `python3 -m venv env`
2. Activate the virtual environment: `source env/bin/activate`
2. Run `pip install --upgrade 'git+https://github.com/dsabsay/webcomics.git#egg=webcomics&subdirectory=app'`
3. Configure the app by editing `env/var/webcomics-instance/config.py`. See [Configuration](#configuration) below for what to include.
4. Run `gunicorn --bind=127.0.0.1:4020 --workers=2 --daemon --pidfile=gunicorn.pid 'webcomics:create_app()'`
5. Set up NGINX to proxy requests to gunicorn.
6. Initialize the database if you will be using a new one: `export FLASK_APP=webcomics; flask init-db`
6. Ensure you have configured a deploy key on the `DB_BACKUP_REMOTE_REPO` and that the private key is available at `DB_BACKUP_DEPLOY_KEY`.
7. Start the `webcomicsd` background worker process: `flask webcomicsd start`

All logs are stored in the application instance folder. This is `var/webcomics-instance/` inside the virtual environment directory. The PID file for `webcomicsd` is also stored here.

### Configuration
The app has the following configuration parameters.

| Name                  | Required | Description                                                                                                                                           | Example                                     |
|-----------------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
| DATABASE              | Yes      | Absolute path to databse file.                                                                                                                        | "/home/myuser/webcomics/db.sqlite"          |
| DB_BACKUP_LOCAL_REPO  | Yes      | Absolute path to local repo to hold database backup.                                                                                                  | "/home/myuser/webcomics/db"                 |
| DB_BACKUP_REMOTE_REPO | Yes      | URI to remote repo where backups will be pushed.                                                                                                      | "git@github.com:dsabsay/test-db-backup.git" |
| DB_BACKUP_DEPLOY_KEY  | Yes      | Absolute path to SSH deploy key for `DB_BACKUP_REMOTE_REPO`.                                                                                          | "/home/myuser/.ssh/test_deploy_key_rsa"     |
| SECRET_KEY            | Yes      | Secret used to encrypt session data. See [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions) for what to set this to.           | "209rj*$&h41o2i4sakfjas1238asdfj"           |
| DB_BACKUP_INTERVAL    | Yes      | An integer that together with `DB_BACKUP_TIME_UNIT` specifies the frequency of database backups. These periodic backups are run by `webcomicsd`. | 10                                          |
| DB_BACKUP_TIME_UNIT   | Yes      | A string that specifies the unit of time for database backups. One of: `seconds`, `minutes`, `hours`, `days`, or `weeks`.                  | "days"                                      |


## Development Plan
- [x] Bookmarks for narrative-style comics. Can be implemented as a bookmarklet.
- [x] DB backup job
- [x] Why are requests getting logged in `jobs.log`?
- [x] Add CLI command to add a comic.
- [ ] Bookmark enhancement: Smartly handle when the user is not logged in by saving URL temporarily, requesting login, and then saving the bookmark when the user logs in.
- [x] Deploy
- [ ] Implement `reads/` feature to mark strips as read when clicked.
- [ ] Viewer (for webcomic name)
- [ ] RSS feed updater
- [ ] Ability to add new comics. Will require mappings from feed fields -> DB columns.

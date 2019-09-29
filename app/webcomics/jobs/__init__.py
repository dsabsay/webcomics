import datetime
import time
import logging
import traceback
import signal
import os

import daemonize
import schedule
from flask import current_app
import psutil

from webcomics.jobs.backup_db import backup_db_job


# Configure logging for all modules in sub-package
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
handler = logging.handlers.RotatingFileHandler(
    os.path.join(current_app.instance_path, 'jobs.log'),
    maxBytes=4096,
    backupCount=3
)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


PID_FILE = os.path.join(current_app.instance_path, 'webcomicsd.pid')


def main():
    logger.info('Starting work loop...')
    while True:
        schedule.run_pending()
        time.sleep(1)


def start():
    # Keep the log file FD open when daemonizing
    keep_fds = [handler.stream.fileno() for handler in logger.handlers]

    # Set jobs
    schedule.every().day.do(backup_db_job)

    daemon = daemonize.Daemonize(
        app='webcomicsd',
        pid=PID_FILE,
        keep_fds=keep_fds,
        action=main
    )
    daemon.start()


def stop():
    '''
    Attempts to kill the daemon. 

    Returns True if the process exited. Returns False if the
    process does not exit after ~3 seconds.
    '''
    pidfile = open(PID_FILE, 'r')
    pid = int(pidfile.read(-1))
    pidfile.close()

    os.kill(pid, signal.SIGTERM)

    for retry in range(3):
        time.sleep(1)
        if not psutil.pid_exists(pid):
            return True

    return False


def status():
    '''
    Returns a message with information about the status of
    webcomicsd.
    '''
    if not os.path.exists(PID_FILE):
        return 'status: No PID file found.'

    pidfile = open(PID_FILE, 'r')
    pid = int(pidfile.read(-1))
    pidfile.close()

    try:
        p = psutil.Process(pid)
    except psutil.NoSuchProcess as e:
        return f'status: webcomicsd is not running\nPID found: {pid}'

    started = datetime.datetime.fromtimestamp(p.create_time(), tz=datetime.timezone.utc)
    return f'status: {p.status()}\npid: {pid}\nstarted at: {started}'

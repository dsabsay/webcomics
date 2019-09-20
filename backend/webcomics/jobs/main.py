import time
import logging
import traceback
import os

import daemonize
import schedule

from webcomics.jobs.backup_db import backup_db_job


# Configure logging
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
handler = logging.handlers.RotatingFileHandler(
    os.path.join(os.path.expanduser('~'), 'webcomics', 'logs', 'jobs.log'),
    maxBytes=4096,
    backupCount=3
)
handler.setFormatter(formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Keep the log file FD open when daemonizing
keep_fds = [handler.stream.fileno()]

# Set jobs
schedule.every().day.do(backup_db_job)


def main():
    logger.info('Starting event loop...')
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    daemon = daemonize.Daemonize(
        app='webcomicsd',
        pid=os.path.join(os.path.expanduser('~'), 'webcomics', 'webcomicsd.pid'),
        keep_fds=keep_fds,
        action=main
    )
    daemon.start()

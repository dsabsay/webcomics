import logging

from webcomics.db import backup_db

logger = logging.getLogger(__name__)


def backup_db_job():
    try:
        backup_db(isManual=False)
    except Exception as e:
        logger.error('Database backup failed:')
        logger.error(traceback.format_exc())
    else:
        logger.info('Database backup succeeded.')

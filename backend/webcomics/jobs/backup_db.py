from webcomics.db import backup_db


def backup_db_job():
    try:
        backup_db(isManual=False)
    except Exception as e:
        logger.error('Database backup failed:')
        logger.error(traceback.format_exc())
    else:
        logger.info('Database backup succeeded.')

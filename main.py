# - IMPORT ------------------------------------------ #
from utils.loggers import Logger

from config.connection import connection_builder
from models.database.database import Database

from datetime import datetime, timezone

from models.classes.reading_dao import ReadingDao
from utils.export_csv import ExportCSV
# --------------------------------------------------- #


# ------------------ * DATABASE ENGINE * ----------------- #
if __name__ == '__main__':
    Logger.log_info("* "*30)
    Logger.log_info("START: "+datetime.strftime(datetime.utcnow(), '%Y-%m-%d %H:%M:%S'))

    Database.initialize(connection_builder)

    #INPUT:
    fromdate = datetime(2025, 4, 11, 00, 00, 00, tzinfo=timezone.utc)
    todate = datetime(2025, 4, 11, 23, 59, 59, tzinfo=timezone.utc)
    org_id=9

    reading_dao = ReadingDao()
    items_to_export = reading_dao.get_items_to_export(fromdate, todate, [], org_id)

    ExportCSV.send_mail_csv(items_to_export)





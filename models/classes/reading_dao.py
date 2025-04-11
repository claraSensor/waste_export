# IMPORT -------------------------------------------------------
from sqlalchemy.orm import Session

from models.database.database import Database

from utils.loggers import Logger

from sqlalchemy.sql import text

from datetime import datetime

# -------------------------------------------------------------


class ReadingDao:
    STATUS_DEVICE_bool = {}

    STATUS_DEVICE_bool["active"] = True
    STATUS_DEVICE_bool["deactivated"] = False

    def __init__(self):
        try:
            self._db_session: Session = Database.get_session()
        except Exception as exc:
            self._db_session.rollback()
            Logger.log_error(f"database.dao.reading_dao.ReadingDao - {Database.get_db_name()} - init - Exception: {str(exc)}")
            raise exc

    def get_items_to_export(self, fromdate, todate, devices, org_id):
        try:
            #stmt_where = f" "
            #if len(devices) > 0:
            #    devices_string = ', '.join("'"+str(item)+"'" for item in devices)
            #    stmt_where = f" AND lt.terminale in ({devices_string})"

            stmt = text(f'SELECT '
                        f'TO_CHAR(lt.data_ora_utc, \'DD/MM/YYYY\') AS data_svuotamento, '
                        f'am.epc_str AS tag_contribuente, '
                        f'CASE WHEN am.tipo=\'SECCO\' THEN 1 END AS cat_rifiuto, '
                        f'COUNT(lt.epc) AS num_svuotamenti, '
                        f'0 AS kg, '
                        f'\'\' AS nota '
                        f'FROM letture lt '
                        f'INNER JOIN dispositivi d ON (lt.terminale = d.seriale) '
                        f'INNER JOIN organizations_devices od ON (d.id = od.device_id) '
                        f'INNER JOIN anag_mastelli am ON (od.organization_id = am.organization_id AND lt.epc = am.epc) '
                        f'WHERE lt.msg_type=\'1\' AND od.organization_id = {org_id} AND d.stato = {ReadingDao.STATUS_DEVICE_bool["active"]} '
                        f'AND lt.timestamp_rcv BETWEEN {int(fromdate.timestamp())} AND {int(todate.timestamp())} '
                        f'GROUP BY lt.data_ora_utc, am.epc_str, am.tipo;')

            result = self._db_session.execute(stmt)
            items = [list(row) for row in result.fetchall()]

        except Exception as exc:
            Logger.log_error(f"database.dao.reading_dao.ReadingDao - {Database.get_db_name()} - get_items - Exception: {str(exc)}")
            self._db_session.rollback()
            raise exc
        finally:
            self._db_session.close()
            return items



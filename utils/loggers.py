# ---------------------------------------------------------------------------------------
# - IMPORT - ****************************************************************************
import logging
import pathlib
import datetime
import zipfile
import os
import sys

from config.settings import LOGGER_TO_FILE, LOGGER_APPLICATION_NAME, LOGGER_FORMATTER_STRING, LOGGER_BACKUP_DAYS, LOGGER_PATH
# ---------------------------------------------------------------------------------------

"""
    LOGGER_APPLICATION_NAME: [SPAZI VUOTI: 0, IL SIMBOLO: '_' COME SEPARATORE DELLE VOCI]
        1. PROGETTO: [NUM.CARATTERI: 8]
        2. CLIENTE:  [NUM.CARATTERI: 8]
        3. AMBIENTE: [NUM.CARATTERI: 3] DEV, PRO
        4. VERSIONE: V+[NUM.CARATTERI: 5 di cui il punto ha posizione sempre 2] Example: 000.1, 01.20 
        5. NOTE: [NUM.CARATTERI: 2 SIGLA]
"""

# ---------------------------------------------------------------------------------------
class Logger:

    FORMATTER = logging.Formatter(LOGGER_FORMATTER_STRING)
    @staticmethod
    def log_info(message):
        Logger.logger_writer().info(message)

    @staticmethod
    def log_debug(message):
        Logger.logger_writer().debug(message)

    @staticmethod
    def log_warning(message):
        Logger.logger_writer().warning(message)

    @staticmethod
    def log_error(message):
        Logger.logger_writer().error(message)

    @staticmethod
    def logger_writer():
        try:
            current_date = str(datetime.datetime.now().date()).replace('-', '')
            name = current_date + '__' + LOGGER_APPLICATION_NAME
            log_file_name = LOGGER_PATH + name + ".log"

            logger = logging.getLogger(name)
            if len(logger.handlers) == 0:

                handler = logging.StreamHandler(sys.stdout)
                if LOGGER_TO_FILE:
                    handler = logging.FileHandler(log_file_name)

                logging._acquireLock()
                handler.setFormatter(Logger.FORMATTER)

                logger.setLevel(logging.DEBUG)
                logger.addHandler(handler)

                if LOGGER_TO_FILE:
                    Logger.delete_log()
                    Logger.compress_previous_log()

                logging._releaseLock()

        except Exception as exc:
            print(f"{LOGGER_APPLICATION_NAME} - ERROR - Logger - logger_writer: {str(exc)}")
        finally:
            return logger

    @staticmethod
    def delete_log():
        try:
            current_date = datetime.datetime.now().date()

            num_deleted_logs = 0
            days = datetime.timedelta(LOGGER_BACKUP_DAYS)
            date_str = str(current_date - days).replace('-', '')
            date_int = int(date_str)

            arr_logs = os.listdir(LOGGER_PATH)
            for elm_file in arr_logs:
                try:
                    if elm_file.endswith('.log') or elm_file.endswith('.zip'):
                        elm_filename = elm_file.split("__")
                        if len(elm_filename) > 1:
                            filename_date_int = int(elm_filename[0])
                            if filename_date_int < date_int:
                                num_deleted_logs += 1
                                os.remove(LOGGER_PATH + elm_file)
                except Exception as exc:
                    print(f"{LOGGER_APPLICATION_NAME} - ERROR - Logger - delete_log for di arr_logs: {str(exc)}")
                    continue
        except Exception as exc:
            print(f"{LOGGER_APPLICATION_NAME} - ERROR - Logger - delete_log: {str(exc)}")
            num_deleted_logs = 0
        finally:
            return num_deleted_logs

    @staticmethod
    def compress_previous_log():
        try:
            current_date_str_num = str(datetime.datetime.now().date()).replace('-', '')

            num_compressed_logs = 0

            current_date_int = int(current_date_str_num)

            arr_logs = os.listdir(LOGGER_PATH)

            for elm_file in arr_logs:
                try:
                    if elm_file.endswith('.log'):
                        elm_filename = elm_file.split("__")
                        if len(elm_filename) > 1 and elm_file.endswith('.log'):
                            filename_date_int = int(elm_filename[0])
                            if filename_date_int > 0 and filename_date_int != current_date_int:
                                # if filename_date_int != current_date_int:
                                filename_in = elm_file
                                filename_in_path = LOGGER_PATH + elm_file
                                filename_out_path = filename_in_path.replace('.log', '.zip')

                                zf = zipfile.ZipFile(filename_out_path, mode="w")
                                zf.write(filename_in_path, filename_in, compress_type=zipfile.ZIP_DEFLATED)

                                zf.close()
                                os.remove(filename_in_path)
                                num_compressed_logs += 1
                except Exception as exc:
                    print(f"{LOGGER_APPLICATION_NAME} - ERROR - Logger - compress_logs for di arr_logs: {str(exc)}")
                    continue

        except Exception as exc:
            print(f"{LOGGER_APPLICATION_NAME} - ERROR - Logger - compress_logs: {str(exc)}")
            num_compressed_logs = False
        finally:
            return num_compressed_logs

    # --------------------------------------------------------------------------------------------------
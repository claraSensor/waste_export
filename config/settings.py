import os
from pathlib import Path

# ----------------------------------------------------------- #
# >>> Database

DB_HOST = os.getenv("DB_HOST", "")
DB_USER = os.getenv("DB_USER", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "")
DB_PORT = int(os.getenv("DB_PORT", "5432"))

ENGINE_ECHO = False
# ----------------------------------------------------------- #


# --------------------------------------------------------------- #
LOGGER = True
LOGGER_TO_FILE = True
LOGGER_APPLICATION_NAME = 'BR0WASTE_00000000_DEV_V00.01_00'
LOGGER_FORMATTER_STRING = '%(asctime)s - %(levelname)s - %(message)s'
LOGGER_PATH = str(Path(__file__).parent.parent.absolute()) + '/logs/'
LOGGER_BACKUP_DAYS = 7

# --------------------------------------------------------------- #


# ----------------------------------------------------------- #
# >>> SEND MAIL

EMAIL_USE_SSL = True
EMAIL_HOST = ''
EMAIL_PORT = 465
EMAIL_SENDER_USER = ''
EMAIL_SENDER_PASSWORD = ''


EMAIL_FROM = ""
EMAIL_PASSWORD = ""

EMAIL_RECEIVERS = ['clara.iscaro@sensorid.it']


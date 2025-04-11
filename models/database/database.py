# - IMPORT ------------------------------------------ #
from utils.loggers import Logger

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.exc import OperationalError

from models.database.connection_builder import ConnectionBuilder

from config.settings import ENGINE_ECHO, LOGGER

import time
# --------------------------------------------------- #

class Base(DeclarativeBase):
    pass

class Database:

    SLEEP_TWENTY_SECOND = 20.0

    _engine = None
    _session = None
    _base = None

    @staticmethod
    def get_engine():
        return Database._engine

    @staticmethod
    def get_session():
        return Database._session

    @staticmethod
    def get_base():
        return Database._base

    @staticmethod
    def initialize(connection_builder: ConnectionBuilder):
        try:
            Database._engine = create_engine(f"postgresql+psycopg2://{connection_builder.username}:{connection_builder.password}"
                                             f"@{connection_builder.host}:{connection_builder.port}/"
                                             f"{connection_builder.database}", echo=ENGINE_ECHO)

            Session = sessionmaker(bind=Database._engine)
            session = Session()
            Database._session = session
            Database._base = Base()

            if LOGGER:
                Logger.log_info(f"models - database - Database - inizialize - Session:: {session}")
        except Exception as ex:
            Logger.log_error(f"models - database - Database - inizialize - Exception: {str(ex)}")

    @staticmethod
    def reconnect(connection_builder: ConnectionBuilder):
        while True:
            try:
                Database.initialize(connection_builder)
                if Database.is_connection_open(Database.get_session()):
                    if LOGGER:
                        Logger.log_info("models - database - Database - reconnect - Connection reestablished")
                    break
            except Exception as ex:
                Logger.log_error(f"models - database - Database - reconnect - Exception: {str(ex)}")
            time.sleep(Database.SLEEP_TWENTY_SECOND)

    @staticmethod
    def is_connection_open(session):
        try:
            session.execute(text('SELECT 1'))
            return True
        except OperationalError as ex:
            Logger.log_error(f"models - database - Database - reconnect - Exception: Database connection is not open: {str(ex)}")
            return False


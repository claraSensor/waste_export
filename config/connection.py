# - IMPORT ------------------------------------------ #
from models.database.connection_builder import ConnectionBuilder
from config.settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
# --------------------------------------------------- #

connection_builder = ConnectionBuilder()
connection_builder.username = DB_USER
connection_builder.password = DB_PASSWORD
connection_builder.host = DB_HOST
connection_builder.port = DB_PORT
connection_builder.database = DB_NAME
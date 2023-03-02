import os
import sys

from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)


class ReconnectMysqlDatabase(ReconnectMixin, PooledMySQLDatabase):
    def sequence_exists(self, seq):
        pass


MYSQL_HOST = "127.0.0.1"
MYSQL_DB = "ms"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
DB = ReconnectMysqlDatabase(MYSQL_DB, host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD)


SERVER_PORT = "50051"

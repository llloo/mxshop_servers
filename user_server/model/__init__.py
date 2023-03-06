from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin


from ..settings import settings


class ReconnectMysqlDatabase(ReconnectMixin, PooledMySQLDatabase):
    def sequence_exists(self, seq):
        pass


DB = ReconnectMysqlDatabase(settings.MYSQL_DB, host=settings.MYSQL_HOST, user=settings.MYSQL_USER,
                            password=settings.MYSQL_PASSWORD)

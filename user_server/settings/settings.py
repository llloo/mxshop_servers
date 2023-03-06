import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

DEBUG = True

MYSQL_HOST = "127.0.0.1"
MYSQL_DB = "ms"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"


SERVER_PORT_TEST = '50051'

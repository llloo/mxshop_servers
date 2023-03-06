from concurrent import futures

from loguru import logger
import grpc

from settings import settings  # noqa

from handler.user import UserService
from handler.health import HealthServicer
from health.v1 import health_pb2_grpc
from protos import user_pb2_grpc
from utils.base import get_free_socket_port

logger.add("logs/user.log", rotation="50 MB", backtrace=True, diagnose=True)

SERVER_PORT = get_free_socket_port()


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    user_pb2_grpc.add_UserServicer_to_server(UserService(), server)
    logger.info("注册用户服务")

    health_pb2_grpc.add_HealthServicer_to_server(HealthServicer(), server)
    logger.info("注册健康检查服务")

    server.add_insecure_port(f'[::]:{SERVER_PORT}')
    server.start()
    logger.info(f"服务启动成功, PORT: {SERVER_PORT}")
    server.wait_for_termination()


if __name__ == '__main__':
    run()

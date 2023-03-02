from concurrent import futures

from loguru import logger
import grpc

from settings import settings
from handler.user import UserService
from protos import user_pb2_grpc

logger.add("logs/user.log", rotation="50 MB", backtrace=True, diagnose=True)


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    user_pb2_grpc.add_UserServicer_to_server(UserService(), server)
    logger.info("注册用户服务")

    server.add_insecure_port('[::]:' + settings.SERVER_PORT)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    run()

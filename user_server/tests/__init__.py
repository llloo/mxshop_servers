from concurrent import futures

import grpc
from loguru import logger

from ..settings import settings
from protos import user_pb2_grpc
from health.v1 import health_pb2_grpc
from user_server.handler import user, health


class Service:
    def __init__(self):
        self.server = None

    def start_server(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        user_pb2_grpc.add_UserServicer_to_server(user.UserService(), server)
        health_pb2_grpc.add_HealthServicer_to_server(health.HealthServicer(), server)
        server.add_insecure_port(f'[::]:{settings.SERVER_PORT_TEST}')
        server.start()
        self.server = server
        logger.info(f"启动服务, port: {settings.SERVER_PORT_TEST}")

    def stop_server(self):
        self.server.stop(None)


service = Service()

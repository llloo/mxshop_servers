from concurrent import futures
from signal import signal, SIGTERM, SIGINT, SIGKILL
import uuid

from loguru import logger
import grpc

from settings import settings  # noqa

from handler.user import UserService
from handler.health import HealthServicer
from health.v1 import health_pb2_grpc
from protos import user_pb2_grpc
from utils.base import get_free_socket_port, get_local_ip
from utils.consul import Consul

logger.add("logs/user.log", rotation="50 MB", backtrace=True, diagnose=True)

SERVER_PORT = get_free_socket_port()
CONSUL = Consul(settings.CONSUL_HOST, settings.CONSUL_PORT)


def register_with_consul(name, service_id, interval="5s", timeout="5s", deregister_critical_service_after="15s"):
    address = get_local_ip()
    consul_check = {
        "name": "Service health status",
        "grpc": f"{address}:{SERVER_PORT}",
        "grpc_use_tls": False,
        "interval": interval,
        "timeout": timeout,
        "DeregisterCriticalServiceAfter": deregister_critical_service_after,
    }
    CONSUL.register(name, service_id=service_id, tags=['grpc', 'python'], address=address,
                    port=SERVER_PORT, check=consul_check)


def deregister_with_consul(server_id):
    CONSUL.deregister(service_id=server_id)


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    user_pb2_grpc.add_UserServicer_to_server(UserService(), server)
    logger.info("注册用户服务")

    health_pb2_grpc.add_HealthServicer_to_server(HealthServicer(), server)
    logger.info("注册健康检查服务")

    server.add_insecure_port(f'[::]:{SERVER_PORT}')
    server.start()
    logger.info(f"服务启动成功, PORT: {SERVER_PORT}")

    service_id = str(uuid.uuid4())
    register_with_consul('mxshop_service', service_id=service_id)

    def handle_sigterm(*_):
        all_rpcs_done_event = server.stop(30)
        all_rpcs_done_event.wait(30)
        # 注销服务
        deregister_with_consul(service_id)

    signal(SIGTERM, handle_sigterm)
    signal(SIGINT, handle_sigterm)
    # signal(SIGKILL, handle_sigterm)
    server.wait_for_termination()


if __name__ == '__main__':
    run()

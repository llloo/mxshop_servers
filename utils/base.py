import socket
from abc import ABC, abstractmethod


class ServiceRegister(ABC):
    """
    服务注册基类
    """
    @abstractmethod
    def register(self, *args, **kwargs):
        """
        服务注册
        :return:
        """

    @abstractmethod
    def deregister(self, *args, **kwargs):
        """
        服务注销
        :return:
        """


def get_free_socket_port() -> int:
    """
    获取一个本地可用的端口号
    :return:
    """
    s = socket.socket()
    s.bind(('', 0))
    _, port = s.getsockname()
    s.close()
    return port


def get_local_ip():
    """
    获取本地 ip
    :return:
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


if __name__ == '__main__':
    print(get_free_socket_port())

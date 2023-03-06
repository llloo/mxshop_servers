import socket


def get_free_socket_port() -> int:
    """
    获取一个本地可用的端口号
    :return:
    """
    sock = socket.socket()
    sock.bind(('', 0))
    _, port = sock.getsockname()
    sock.close()
    return port


if __name__ == '__main__':
    print(get_free_socket_port())

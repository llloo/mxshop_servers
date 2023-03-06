import sys

from loguru import logger
import requests

from .base import ServiceRegister


class Consul(ServiceRegister):
    headers = {
        "ContentType": "application/json"
    }

    def register(self, name, service_id=None, address=None, port=None, tags=None,
                 check=None, token=None, meta=None):

        payload = {
            'name': name
        }
        if service_id:
            payload['id'] = service_id
        if address:
            payload['address'] = address
        if port:
            payload['port'] = port
        if tags:
            payload['tags'] = tags
        if check:
            payload['check'] = check
        if meta:
            payload['meta'] = meta

        headers = self.headers
        if token:
            headers['X-Consul-Token'] = token

        url = f"http://{self.host}:{self.port}/v1/agent/service/register"  # noqa
        resp = requests.put(url, headers=self.headers, json=payload)
        if resp.status_code == 200:
            logger.info("服务注册成功")
        else:
            logger.error("服务注册失败")
            sys.exit(1)

    def deregister(self, service_id, **kwargs):
        url = f"http://{self.host}:{self.port}/v1/agent/service/deregister/{service_id}"  # noqa
        resp = requests.put(url, headers=self.headers)
        if resp.status_code == 200:
            logger.info("服务注销成功")
        else:
            logger.error("服务注销失败")

    def __init__(self, host, port):
        self.host = host
        self.port = port

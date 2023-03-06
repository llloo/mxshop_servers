import grpc

from health.v1 import health_pb2, health_pb2_grpc

from ..settings import settings
from . import service


class TestHealth:

    def setup_class(self):
        service.start_server()
        self.channel = grpc.insecure_channel(f"localhost:{settings.SERVER_PORT_TEST}")
        self.stub = health_pb2_grpc.HealthStub(self.channel)

    def teardown_class(self):
        self.channel.close()
        service.stop_server()

    def test_check(self):
        resp = self.stub.Check(health_pb2.HealthCheckRequest())

        assert isinstance(resp, health_pb2.HealthCheckResponse)
        assert resp.status == 1

import grpc

from ..settings import settings
from health.v1 import health_pb2, health_pb2_grpc


class TestHealth:

    def setup_class(self):
        self.channel = grpc.insecure_channel("localhost:" + settings.SERVER_PORT)
        self.stub = health_pb2_grpc.HealthStub(self.channel)

    def teardown_class(self):
        self.channel.close()

    def test_check(self):
        resp = self.stub.Check(health_pb2.HealthCheckRequest())

        assert isinstance(resp, health_pb2.HealthCheckResponse)
        assert resp.status == 1

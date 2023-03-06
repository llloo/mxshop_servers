import random

import pytest
from google.protobuf import empty_pb2
import grpc

from ..settings import settings
from protos import user_pb2_grpc, user_pb2
from . import service


class TestUser:

    def setup_class(self):
        service.start_server()
        self.channel = grpc.insecure_channel(f"localhost:{settings.SERVER_PORT_TEST}")
        self.stub = user_pb2_grpc.UserStub(self.channel)

        self.nick_name = "test_nick_name"
        self.password = "test_password"
        self.mobile = "12345678910"
        self.gender = random.randint(0, 1)

    def teardown_class(self):
        self.channel.close()
        service.stop_server()

    def test_create_user(self):
        create_user_info = user_pb2.CreateUserInfoRequest(
            nickName=self.nick_name,
            password=self.password,
            mobile=self.mobile,
            gender=self.gender,
        )
        user = self.stub.createUser(create_user_info)

        assert isinstance(user, user_pb2.UserInfoResponse)
        assert user.nickName == self.nick_name
        assert user.mobile == self.mobile
        assert user.gender == self.gender

    def test_get_user_list(self):
        page = 1
        page_size = 10
        user_list = self.stub.getUserList(user_pb2.PageInfoRequest(page=page, pageSize=page_size))

        assert isinstance(user_list, user_pb2.UserListResponse)
        assert user_list.page.page == page
        assert user_list.page.pageSize == page_size
        assert len(user_list.data) == page_size

    def test_get_user_by_id(self):
        user_id = 1
        user = self.stub.getUserById(user_pb2.UserIdRequest(id=user_id))

        assert isinstance(user, user_pb2.UserInfoResponse)
        assert user.id == user_id
        assert user.mobile

    def test_get_user_by_mobile(self):
        user = self.stub.getUserByMobile(user_pb2.UserMobileRequest(mobile=self.mobile))

        assert isinstance(user, user_pb2.UserInfoResponse)
        assert user.mobile == self.mobile

    def test_update_user(self):
        user = self.stub.getUserByMobile(user_pb2.UserMobileRequest(mobile=self.mobile))

        new_nick_name = "new_nick_name"
        resp = self.stub.updateUser(user_pb2.UpdateUserInfoRequest(
            id=user.id,
            nickName=new_nick_name
        ))

        assert isinstance(resp, empty_pb2.Empty)

        user = self.stub.getUserById(user_pb2.UserIdRequest(id=user.id))
        assert user.nickName == new_nick_name

    def test_mobile_login(self):
        resp = self.stub.mobileLogin(user_pb2.MobileLoginRequest(mobile=self.mobile, password=self.password))

        assert isinstance(resp, user_pb2.LoginResultResponse)
        assert resp.success

    def test_delete_user(self):
        user = self.stub.getUserByMobile(user_pb2.UserMobileRequest(mobile=self.mobile))

        resp = self.stub.deleteUser(user_pb2.UserIdRequest(id=user.id))
        assert isinstance(resp, empty_pb2.Empty)

        with pytest.raises(grpc.RpcError) as rpc_error:
            self.stub.getUserById(user_pb2.UserIdRequest(id=user.id))

            assert rpc_error.code() == grpc.StatusCode.NOT_FOUND  # noqa

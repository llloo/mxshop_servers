import time
from datetime import datetime

from google.protobuf import empty_pb2
import grpc
import peewee
from loguru import logger

from user_server.model.models import User, make_password
from protos import user_pb2, user_pb2_grpc


class UserService(user_pb2_grpc.UserServicer):

    @staticmethod
    def serializer_user(info: user_pb2.UserInfoResponse, user: User) -> user_pb2.UserInfoResponse:
        info.id = user.id
        info.mobile = user.mobile
        info.gender = user.gender
        info.role = user.role
        if user.nick_name:
            info.nickName = user.nick_name
        if user.avatar:
            info.avatar = user.avatar
        if user.birthday:
            info.birthday = int(time.mktime(user.birthday.timetuple()))
        if user.address:
            info.address = user.address
        return info

    @logger.catch
    def getUserList(self, request, context):
        page = request.page or 1
        page_size = request.pageSize or 10

        users = User.select().order_by('id').paginate(page, page_size)
        user_list = user_pb2.UserListResponse()
        user_list.page.page = page
        user_list.page.pageSize = page_size
        for u in users:
            info = user_pb2.UserInfoResponse()
            info = self.serializer_user(info, u)
            user_list.data.append(info)
        return user_list

    @logger.catch
    def getUserById(self, request, context):
        user_id = request.id
        user_info = user_pb2.UserInfoResponse()
        try:
            user = User.get(id=user_id)
            user_info = self.serializer_user(user_info, user)
            return user_info
        except peewee.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('用户不存在')
            return user_info

    @logger.catch
    def getUserByMobile(self, request, context):
        mobile = request.mobile
        user_info = user_pb2.UserInfoResponse()
        try:
            user = User.get(mobile=mobile)
            user_info = self.serializer_user(user_info, user)
            return user_info
        except peewee.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('用户不存在')
            return user_info

    @logger.catch
    def createUser(self, request, context):
        info = user_pb2.UserInfoResponse()
        try:
            User.get(mobile=request.mobile)
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("用户已经存在")
            return info
        except peewee.DoesNotExist:
            user = User()
            user.nick_name = request.nickName
            user.password = make_password(request.password)
            user.mobile = request.mobile
            user.gender = request.gender
            user.role = 1
            user.save()
            return self.serializer_user(info, user)

    @logger.catch
    def updateUser(self, request, context):
        user_id = request.id
        try:
            user = User.get(id=user_id)
            if request.nickName:
                user.nick_name = request.nickName
            if request.avatar:
                user.avatar = request.avatar
            if request.birthday:
                user.birthday = datetime.fromtimestamp(request.birthday).date()
            if request.address:
                user.address = request.address
            if request.desc:
                user.desc = request.desc
            if request.gender:
                user.gender = request.gender
            user.save()
            return empty_pb2.Empty()
        except peewee.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户不存在")
            return empty_pb2.Empty()

    @logger.catch
    def deleteUser(self, request, context):
        user_id = request.id
        try:
            user = User.get(id=user_id)
            user.delete_instance()
            return empty_pb2.Empty()
        except peewee.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("用户不存在")
            return empty_pb2.Empty()

from passlib.hash import pbkdf2_sha256
from peewee import *

from user_server.settings import settings


def make_password(raw_password):
    return pbkdf2_sha256.hash(raw_password)


class BaseModel(Model):
    class Meta:
        database = settings.DB


class User(BaseModel):
    USER_GENDER_CHOICES = [
        (0, "male"),
        (1, "female"),
    ]
    USER_ROLE_CHOICES = [
        (0, "admin"),
        (1, "user"),
    ]
    mobile = CharField(max_length=11, index=True, unique=True, verbose_name="手机号")
    password = CharField(max_length=100)
    nick_name = CharField(max_length=20, null=True)
    avatar = CharField(max_length=300, null=True)
    birthday = DateField(null=True)
    address = CharField(max_length=300, null=True)
    desc = TextField(null=True)
    gender = SmallIntegerField(choices=USER_GENDER_CHOICES, null=True)
    role = SmallIntegerField(choices=USER_ROLE_CHOICES, default=1)

    def set_password(self, raw_password: str):
        pass_hash = pbkdf2_sha256.hash(raw_password)
        self.password = pass_hash
        self.save()

    def check_password(self, raw_password):
        return pbkdf2_sha256.verify(raw_password, self.password)


if __name__ == '__main__':
    pass
    # settings.DB.create_tables([User])
    # from passlib.hash import pbkdf2_sha256
    # for i in range(100):
    #     u = User()
    #     u.mobile = str(10000000000 + i)
    #     u.password = pbkdf2_sha256.hash(u.mobile)
    #     u.nick_name = f'user-{i}'
    #     u.gender = random.randint(0, 1)
    #     u.role = 1
    #     u.save()

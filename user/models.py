from django.db import models


class UserModel(models.Model):

    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=64, unique=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'ttasx_users'


class UserTicketModel(models.Model):

    # 关联用户表
    user = models.ForeignKey(UserModel)
    # ticket设置
    ticket = models.CharField(max_length=256)
    # 过期时间
    out_time = models.DateTimeField()

    class Meta:
        db_table = 'ttasx_users_ticket'

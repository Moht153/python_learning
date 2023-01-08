from django.db import models

# Create your models here.

# class -> UserProfile
# 表名 user_profile
# 字段 username, nickname,email,password,sign,info,avatar


class UserProfile(models.Model):
	username = models.CharField(max_length=11, primary_key=True, verbose_name='用户姓名')
	email = models.CharField(max_length=50, verbose_name='邮箱', null=True)
	password = models.CharField(max_length=32)
	avatar = models.ImageField(upload_to='avatar/')

	class Meta:
		db_table = 'user'
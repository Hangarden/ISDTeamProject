# class AbstractBaseUser(models.Model):
#     password = models.CharField(max_length=128)
# 	last_login = models.DateTimeField(blank=True, null=True)
# 	...
#
# class PermissionsMixin(models.Model):
#     is_superuser = models.BooleanField(default=False)
# 	...
#
# class AbstractUser(AbstractBaseUser, PermissionsMixin):
# 	username = models.CharField(max_length=150, unique=True)
# 	first_name = models.CharField(max_length=30, blank=True)
# 	last_name = models.CharField(max_length=30, blank=True)
# 	email = models.EmailField(blank=True)
# 	is_staff = models.BooleanField(default=False)
# 	is_active = models.BooleanField(default=False) # 로그인 허용 여부
# 	date_joined = models.DateTimeField(default=timezone.now)
#
# from django.conf import settings # 추천!
# from django.conf.auth.models import User # 비추
# from django.db import models
#
# class Post(models.Model):
# 	author = models.ForeignKey(User) 		# 비추
# 	author = models.ForeignKey('auth.User') # 비추
# 	author = models.ForeignKey(settings.AUTH_USER_MODEL) #

from django.db import models
from django.contrib.auth.models import  User
from map.models import MapCity

class Residence(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.ForeignKey(MapCity, on_delete=models.CASCADE)
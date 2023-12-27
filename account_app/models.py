from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager


class User(AbstractBaseUser):
    username = models.CharField(max_length=40, unique=True, verbose_name="نام کاربری")
    email = models.EmailField(verbose_name="ایمیل")
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_admin = models.BooleanField(default=False, verbose_name='مدیر')
    objects = UserManager()
    USERNAME_FIELD = 'username'
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربر ها'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

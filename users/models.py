from django.db import models
from django.contrib.auth.models import User


class MyUser(User):
    class Meta:
        proxy = True
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

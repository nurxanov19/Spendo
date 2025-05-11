from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(blank=True, null=True, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True, unique=True)
    username = models.CharField(max_length=200, unique=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    avatar = models.ImageField(upload_to='users/', default='user_logo.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def clean(self):
    #     if not self.email or not self.phone:
    #         raise ValidationError('Either Email or Phone must be entered')

    class Meta:
        verbose_name = 'customuser'
        verbose_name_plural = 'customusers'

    def __str__(self):
        return self.username





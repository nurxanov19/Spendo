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


class OneTimePasswordModel(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    key = models.CharField(max_length=200)
    is_expired = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)
    tried = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.email and not self.phone:
            raise ValidationError("Either phone or email must be provided.")
        if self.email and self.phone:
            raise ValidationError("Only one of phone or email should be provided.")

    def save(self, *args, **kwargs):
        if self.tried > 3:
            self.is_expired = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OTP for {self.email or self.phone} - Expired: {self.is_expired}"


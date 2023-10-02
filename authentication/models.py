from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
USER_TYPE_CHOICES = (
    ("superadmin", "Super Admin"),
    ("lspp", "Leapfrog Student Partner"),
    ("user", "User"),
)


class User(AbstractUser):
    email = models.EmailField(unique=True)
    type = models.CharField(max_length=30, choices=USER_TYPE_CHOICES, default="user")
    otp = models.CharField(max_length=6, null=True, blank=True)


class BlackListedToken(models.Model):
    token = models.CharField(max_length=255, unique=True)

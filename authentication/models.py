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


class Profile(models.Model):
    def upload_profile_picture(instance, filename):
        return f"profile/{instance.user.username}/{filename}"

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to=upload_profile_picture, blank=True, null=True)
    college = models.CharField(max_length=100, blank=True, null=True)
    batch = models.IntegerField(blank=True, null=True)
    website_url = models.CharField(max_length=500, blank=True, null=True)
    linkedin_url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.user.username

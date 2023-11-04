from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post"
    )  # reference from Users

    def __str__(self):
        return self.title


class Comments(models.Model):
    post = models.ForeignKey(
        Posts, on_delete=models.CASCADE,related_name="comment_post"
    )  # reference from Posts
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_user"
    )  # reference from Users
    c_content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}/{self.post}"


class Likes(models.Model):
    post = models.ForeignKey(
        Posts, on_delete=models.CASCADE, related_name="like_post"
    )  # refrence from Posts
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="like_user"
    )  # reference from Users
    created_at = models.DateTimeField(auto_now=True)

from django.contrib.auth.models import User
from rest_framework import serializers

from authentication.serializers import *

from .models import *


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = "__all__"

        read_only_fields = ["user","post"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"

        read_only_fields = ["user"]


class CommentEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = "__all__"

        read_only_fields = ["user","post"]


class PostSerializer(serializers.ModelSerializer):
    comment_post = CommentSerializer(many=True)
    like_post = LikeSerializer(many=True)
    user = serializers.CharField()

    class Meta:
        model = Posts
        fields = (
             "user",
             "post_id",
             "title",
             "content",
             "created_at",
             "updated_at",
             "comment_post",
             "like_post",
         )


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ("user","title","content")

        read_only_fields = ["user"]

from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from blogs.serializers import (
    CommentEditSerializer,
    CommentSerializer,
    CreatePostSerializer,
    LikeSerializer,
    PostSerializer,
)
from core.response import CustomResponse as cr

from .models import Comments, Likes, Posts


class GetBlogView(APIView):
    serializer_class = PostSerializer

    def get(self, request: Request) -> Response:
        """
        Get the information about a blog post.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object.
        """

        posts = Posts.objects.all()
        serializer = self.serializer_class(posts, many=True)
        return cr.success(data=serializer.data, message="Blogs fetched successfully!")

    def get(self, request: Request, post_id) -> Response:
        """
        Get the information about a blog post.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object.
        """

        posts = Posts.objects.filter(post_id=post_id).first()
        if not posts:
            return cr.error(message="Post not found.")
        serializer = self.serializer_class(posts)
        return cr.success(data=serializer.data, message="Blog fetched successfully!")


class CreateBlogView(APIView):
    permission_classes = [IsAuthenticated]

    serializer_class = CreatePostSerializer

    def post(self, request: Request) -> Response:
        """
        Post a new blog.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object.
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)

        return cr.success(data=serializer.data, message="New blog added successfully!")

    def put(self, request: Request, post_id) -> Response:
        """
        Update the comments.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object containing the new access token.
        """

        post = Posts.objects.filter(post_id=post_id, user=request.user).first()
        if not post:
            return cr.error("Post not found.")

        serializer = self.serializer_class(post, data=request.data)
        serializer.is_valid(raise_exception=True)

        save = serializer.save(user=request.user)

        return cr.success(data=serializer.data, message="Post updated successfully!")

    def delete(self, request: Request, post_id) -> Response:
        """
        Delete the posts.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object.
        """

        post = Posts.objects.filter(post_id=post_id, user=request.user).first()
        if not post:
            return cr.error(message="Post not found.")

        post.delete()
        return cr.success(message="Post deleted successfully.")


class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    serializer_class = CommentSerializer

    def post(self, request: Request) -> Response:
        """
        Post a new comment in a post.

        Args:
            request (Request): The HTTP request object.

        Returns:
                Response: The HTTP response object.
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)

        return cr.success(
            data=serializer.data, message="New comment added successfully!"
        )

    def delete(self, request: Request, id) -> Response:
        """
        Delete the comments.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object.
        """

        comment = Comments.objects.filter(id=id, user=request.user).first()
        if not comment:
            return cr.error(message="Comment not found.")

        comment.delete()
        return cr.success(message="Comment deleted successfully.")


class EditCommentView(APIView):
    permission_classes = [IsAuthenticated]

    serializer_class = CommentEditSerializer

    def put(self, request: Request, id) -> Response:
        """
        Update the comments.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object.
        """

        comment = Comments.objects.filter(id=id, user=request.user).first()
        if not comment:
            return cr.error(message="Comment not found.")

        serializer = self.serializer_class(comment, data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return cr.success(data=serializer.data, message="Comment updated successfully!")


class ReadCommentView(APIView):
    serializer_class = CommentSerializer

    def get(self, request: Request, id) -> Response:
        """
        Get the information about a blog post.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object.
        """

        comment = Comments.objects.filter(id=id).first()
        if not comment:
            return cr.error(message="Comment not found.")
        serializer = self.serializer_class(comment)
        return cr.success(data=serializer.data, message="Comment fetched successfully!")


class LikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        """
        Likes the blog post if not liked.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object.
        """
        post = Posts.objects.filter(post_id=post_id).first()
        user = request.user

        if not post:
            return cr.error(message="Post not found.")

        like_exists = Likes.objects.filter(user=user, post=post).exists()
        if like_exists:
            return cr.success(message="You have already liked this post.")

        like = Likes(user=user, post=post)
        like.save()
        return cr.success(message="Post liked successfully.")

    def delete(self, request, post_id):
        """
        Unlike the blog post if liked.

        Args:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object.
        """
        post = Posts.objects.filter(post_id=post_id).first()
        user = request.user

        if not post:
            return cr.error(message="Post not found.")

        like = Likes.objects.filter(user=user, post=post).first()
        if not like:
            return cr.success(message="You have not liked this post.")

        like.delete()
        return cr.success(message="Like removed successfully.")

from django.urls import include, path

from blogs.views import (
    CreateBlogView,
    CreateCommentView,
    EditCommentView,
    GetBlogView,
    LikeView,
    ReadCommentView,
)

urlpatterns = [
    path("getblog/", GetBlogView.as_view()),
    path("readpost/<int:post_id>/", GetBlogView.as_view()),
    path("createblog/", CreateBlogView.as_view()),
    path("createblog/<int:post_id>/", CreateBlogView.as_view()),
    path("deleteblog/<int:post_id>/", CreateBlogView.as_view()),
    path("createcomment/", CreateCommentView.as_view()),
    path("readcomment/<int:id>/", ReadCommentView.as_view()),
    path("editcomment/<int:id>/", EditCommentView.as_view()),
    path("deletecomment/<int:id>/", CreateCommentView.as_view()),
    path("likepost/<int:post_id>/", LikeView.as_view()),
    path("unlikepost/<int:post_id>/", LikeView.as_view()),
]

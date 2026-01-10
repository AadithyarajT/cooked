from django.urls import path
from . import views

urlpatterns = [
    # create a post url
    path("create/", views.create_post, name="create_post"),
    #update a post url
    path("update/<int:post_id>/", views.update_post, name="update_post"),
    # delete a post url
    path("delete/<int:post_id>/", views.delete_post, name="delete_post"),
    #delete comment
    path(
        "delete_comment/<int:comment_id>/", views.delete_comment, name="delete_comment"
    ),
]

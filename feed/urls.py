from django.urls import path
from . import views

urlpatterns = [
    # feed home page
    path("", views.feed_view, name="public_feed"),
    # feed detail page
    path("<int:post_id>/", views.content_view, name="feed_content"),
]

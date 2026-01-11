from django.urls import path
from . import views

urlpatterns = [
    # feed home page
    path("", views.feed_view, name="public_feed"),
    # feed detail page
    path("<int:post_id>/", views.content_view, name="feed_content"),
    path("report/<int:post_id>/", views.report_view, name="report_view"),
    path("reports/", views.view_reports, name="view_reports"),
]

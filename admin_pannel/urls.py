from django.urls import include, path
from .import views

urlpatterns = [
    path("", views.admin_home, name="admin_home"),
    path("send_reply/<int:report_id>/", views.send_report_reply, name="send_report_reply"),
    path("view_users/", views.view_users, name="view_users"),
    path("statistics/", views.view_statistics, name="view_statistics"),
    path("add_topic/", views.add_topics, name="add_topics"),
]

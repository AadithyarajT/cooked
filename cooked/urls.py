
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('posts/', include('posts.urls')),
    path('feed/', include('feed.urls')),
    path('admin_pannel/', include('admin_pannel.urls')),
]

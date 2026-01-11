from django.contrib import admin

# Register your models here.
from . models import Post, comments
from admin_pannel.models import Reports, Topic

admin.site.register(Post)
admin.site.register(comments)
admin.site.register(Reports)
admin.site.register(Topic)
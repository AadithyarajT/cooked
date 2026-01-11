from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Topic(models.Model):
    name = models.CharField(max_length=50)
    usage = models.IntegerField(default=0)

    def __str__(self):
        return self.name

# Create your models here.
class Reports(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    reason = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reply = models.TextField(null=True, blank=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Report by {self.reporter} on {self.post_id.title}"


    

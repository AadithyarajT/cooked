from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User


def default_expiry():
    return timezone.now() + timedelta(days=7)





class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey("admin_pannel.Topic", on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(default=default_expiry)
    is_expired = models.BooleanField(default=False)

    # Score fields
    total_score = models.IntegerField(default=0)
    no_votes = models.IntegerField(default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def average_score(self):
        """Calculate average score"""
        if self.no_votes == 0:
            return 0
        return round(self.total_score / self.no_votes, 1)

    def check_and_mark_expired(self):
        """Check if post is expired and mark it"""
        if timezone.now() > self.expires_at and not self.is_expired:
            self.is_expired = True
            self.save()
            return True
        return False


class ratings(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user.username} rated {self.post.title}: {self.score}"


class comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"


# from django.db import models
# from django.utils import timezone
# from datetime import timedelta
# from django.contrib.auth.models import User


# def default_expiry():
#     return timezone.now() + timedelta(days=7)

# class Topic(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name


# # Create your models here.
# class Post(models.Model):
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
#     title = models.CharField(max_length=100)
#     content = models.TextField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     expires_at = models.DateTimeField(default=default_expiry)
#     is_expired = models.BooleanField(default=False)

#     cooked_score = models.IntegerField(default=0)
#     total_score = models.IntegerField(default=0)
#     no_votes = models.IntegerField(default=0)


#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return self.title

#     def check_and_delete_if_expired(self):
#         """Check if post is expired and delete it"""
#         if timezone.now() > self.expires_at:
#             self.delete()
#             return True
#         return False

# class ratings(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     score = models.IntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     unique_together = ('post', 'user')

# class comments(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     text = models.TextField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f'Comment by {self.author} on {self.post.title}'

from django.shortcuts import render, redirect
from .models import  Post, comments
from .forms import PostForm
from admin_pannel.models import Topic
from django.contrib.auth.decorators import login_required




# Create a post
@login_required
def create_post(request):
    if request.method == "POST":
        created_by = request.user
        topics = request.POST.get("topic_id")
        title = request.POST.get("title")
        content = request.POST.get("content")
        post = Post(
            created_by=created_by, topic=Topic(id=topics), title=title, content=content
        )
        post.save()
        return redirect("public_feed")
    topics = Topic.objects.all()
    context = {"topics": topics}
    return render(request, "posts/post_form.html", context)

# Updating a post
@login_required
def update_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.save()
        return redirect("public_feed")
    context = {"post": post}
    return render(request, "posts/edit_post.html", context)

# Deleting a post
@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.user != post.created_by:
        return redirect("public_feed")

    if request.method == "POST":
        post.delete()
        return redirect("public_feed")
    return render(request, "posts/delete.html", {"obj": post.title})


#delete comment
@login_required
def delete_comment(request, comment_id):
    comment_to = comments.objects.get(id=comment_id)
    if request.user != comment_to.author:
        return redirect("content_view", comment_to.post.id)

    if request.method == "POST":
        comment_to.delete()
        return redirect("feed_content", comment_to.post.id)

    return render(request, "posts/delete.html", {"obj": comment_to.text})

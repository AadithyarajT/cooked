from django.shortcuts import redirect, render
from posts.models import Post, Topic, comments
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# posts feed view
@login_required
def feed_view(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    posts = Post.objects.filter(
        Q(topic__name__icontains=q)&Q(title__icontains=q)|
        Q(content__icontains=q)|
        Q(created_by__username__icontains=q)
        ).order_by('-created_at')

    topics = Topic.objects.all()
    context = {"posts": posts, "topics": topics}
    return render(request, "feed/feed.html", context)


# detail view for individual post
@login_required
def content_view(request, post_id):
    content = Post.objects.get(id=post_id)
    
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        author = request.user
        text = request.POST.get("content")
        post.comments.create(author=author, text=text)
    
        return redirect("feed_content", post_id)
    
    context = {"post": content}
    return render(request, "feed/content.html", context)
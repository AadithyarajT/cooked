from django.shortcuts import redirect, render, get_object_or_404
from posts.models import Post, Topic, comments, ratings
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def feed_view(request):
    q = request.GET.get("q") if request.GET.get("q") != None else ""

    posts = Post.objects.filter(
        Q(topic__name__icontains=q)
        | Q(title__icontains=q)
        | Q(content__icontains=q)
        | Q(created_by__username__icontains=q)
    ).order_by("-created_at")

    topics = Topic.objects.all()
    context = {"posts": posts, "topics": topics}
    return render(request, "feed/feed.html", context)


@login_required
def content_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Check if post is expired
    post.check_and_mark_expired()

    # Get user's existing rating if any
    user_rating = ratings.objects.filter(post=post, user=request.user).first()

    if request.method == "POST":
        # Handle score submission
        if "score" in request.POST and not post.is_expired:
            try:
                score_value = int(request.POST.get("score"))

                if user_rating:
                    # Update existing rating
                    old_score = user_rating.score
                    user_rating.score = score_value
                    user_rating.save()

                    # Update post totals
                    post.total_score = post.total_score - old_score + score_value
                    post.save()
                    messages.success(request, f"Updated your rating to {score_value}!")
                else:
                    # Create new rating
                    ratings.objects.create(
                        post=post, user=request.user, score=score_value
                    )

                    # Update post totals
                    post.total_score += score_value
                    post.no_votes += 1
                    post.save()
                    messages.success(request, f"Rated {score_value}!")

                return redirect("feed_content", post_id)
            except ValueError:
                messages.error(request, "Invalid score value")

        # Handle comment submission
        elif "content" in request.POST:
            text = request.POST.get("content")
            if text.strip():
                post.comments.create(author=request.user, text=text)
                messages.success(request, "Comment added!")
            return redirect("feed_content", post_id)

    context = {
        "post": post,
        "user_rating": user_rating,
        "can_rate": not post.is_expired,
    }
    return render(request, "feed/content.html", context)

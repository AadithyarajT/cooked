from django.shortcuts import redirect, render
from django.contrib.auth.models import User

from admin_pannel.models import Reports, Topic
from posts.models import Post

# Create your views here.
def admin_home(request):
    return render(request, "admin_pannel/admin_home.html")

def send_report_reply(request, report_id):
    report = Reports.objects.get(id=report_id)
    if request.method == "POST":
        reply = request.POST.get("reply")
        report.reply = reply
        report.save()
        return redirect("view_reports") 
    return render(request, "admin_pannel/send_reply.html", {"report": report})

def view_users(request):
    users = User.objects.all()
    context = {"users": users}
    if request.method == "POST":
        delete = request.POST.get("delete")
        block = request.POST.get("block")
        unblock = request.POST.get("unblock")
        if delete:
            user = User.objects.get(id=delete)
            user.delete()
            return redirect("view_users")
        

        
    
    return render(request, "admin_pannel/view_users.html", context)

def view_statistics(request):
    user_count = User.objects.count()
    post_count = Post.objects.count()
    topic_count = Topic.objects.count()
    report_count = Reports.objects.count()
    context = {"user_count": user_count, "post_count": post_count, "topic_count": topic_count, "report_count": report_count}    
    return render(request, "admin_pannel/statistics.html", context)

def add_topics(request):
    topic = Topic(name=request.POST.get("topic_name"))
    if request.method == "POST":
        topic = Topic(name=request.POST.get("topic_name"))
        topic.save()
        return redirect("view_topics")
    context = {'topic': topic}
    return render(request, "admin_pannel/add_topic.html", context)

from django.shortcuts import redirect, render
from django.contrib import messages
from base import models
from posts.models import Post
from admin_pannel.models import Topic
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# login page
def loginget(request):
    return render(request, "base/login.html")

# login page check

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def loginPage(request):
    # If user is already logged in, redirect them
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        # Get credentials
        username_or_email = request.POST.get("username") or request.POST.get("email")
        password = request.POST.get("password")

        # Basic validation
        if not username_or_email or not password:
            messages.error(request, "Please provide both username/email and password")
            return render(request, "base/login.html")

        user = None

        try:
            # First try to authenticate with username
            user = authenticate(request, username=username_or_email, password=password)

            # If that fails and input contains '@', try with email
            if user is None and "@" in username_or_email:
                try:
                    # Get user by email
                    user_by_email = User.objects.get(email=username_or_email)
                    # Try authenticating with the username from that email
                    user = authenticate(
                        request, username=user_by_email.username, password=password
                    )
                except User.DoesNotExist:
                    pass  # User with this email doesn't exist

        except Exception as e:
            # Log the error for debugging (in production, use proper logging)
            print(f"Login error: {e}")
            messages.error(request, "An error occurred during login")
            return render(request, "base/login.html")

        # Check if authentication was successful
        if user is not None:
            # User is valid, check if active
            if user.is_active:
                login(request, user)

                # Add success message
                messages.success(request, f"Welcome back, {user.username}!")

                # Redirect based on user type
                if user.is_staff or user.is_superuser:
                    return redirect("admin_home")  # Make sure this URL exists
                else:
                    return redirect("home")  # Regular user home
            else:
                messages.error(request, "Your account is disabled")
        else:
            messages.error(request, "Invalid username/email or password")

        return render(request, "base/login.html")

    # GET request - show login form
    return render(request, "base/login.html")


# register page
def registergget(request):
    return render(request, "base/register.html")

# register page check
def registerPage(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    confirm_password = request.POST.get("confirm_password")
    if request.method == "POST":
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, "base/register.html")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return render(request, "base/register.html")
        else:
            if password != confirm_password:
                messages.error(request, "Passwords do not match")
                return render(request, "base/register.html")
            else:
                user = User.objects.create_user(username, email, password)
                user.save()
                messages.success(request, "User created successfully")
                return redirect("login")
    return render(request, "base/register.html")

def logoutuser(request):
    logout(request)

    context = {}
    return render(request, "base/login.html", context)


# Create your views here.
def home(request):

    return render(request, "base/home.html")


@login_required(login_url="login")
def view_profile(request):
    # Get posts created by the current user
    user_posts = Post.objects.filter(created_by=request.user).order_by("-created_at")

    # Get cooked scores for user's posts
    # for post in user_posts:
    #     # Calculate average score for each post
    #     if post.scores.exists():
    #         post.average_score = post.scores.aggregate(models.Avg("score"))[
    #             "score__avg"
    #         ]
    #     else:
    #         post.average_score = None

    context = {
        "user": request.user,
        "posts": user_posts,
        "post_count": user_posts.count(),
    }
    return render(request, "base/profile.html", context)


@login_required(login_url="login")
def update_profile(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        user = request.user
        user.username = username
        user.email = email
        user.save()
        return redirect("view_profile")

    return render(request, "base/update_profile.html")


@login_required(login_url="login")
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = request.user
        if not user.check_password(current_password):
            messages.error(request, "Current password is incorrect")
            print("Current password is incorrect")
            return render(request, "base/changepassword.html")
        if new_password != confirm_password:
            messages.error(request, "New passwords do not match")
            print("New passwords do not match")
            return render(request, "base/changepassword.html")
        else:
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password changed successfully")
            print("Password changed successfully")
            return redirect("login")
        
    return render(request, "base/changepassword.html")



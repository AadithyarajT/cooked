from django.urls import path
from . import views

urlpatterns = [
    #authentication routes
    path('login/', views.loginPage, name='login'),
    path('login_get/', views.loginget, name='loginget'),
    path('logout/', views.logoutuser, name='logoutuser'),
    #registration routes
    path('register/', views.registerPage, name='register'),
    path('register_get/', views.registergget, name='registergget'),
    #home page
    path('', views.home, name='home'),
    #profile routes
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    #change password route
    path('change_password/', views.change_password, name='change_password'),
]

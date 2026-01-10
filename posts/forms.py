from django import forms
from django.forms import ModelForm
from .models import Post, comments


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        


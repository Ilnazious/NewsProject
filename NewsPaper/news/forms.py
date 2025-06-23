from django import forms
from .models import Post
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text',]

class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common_group = Group.objects.get(name='common')
        user.groups.add(common_group)
        return user
from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'image', 'is_published']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'login'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'pas1'}))
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'class': 'pas2'}))
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']



class LoginUserForm(AuthenticationForm):
    class Meta:
        model = User
        field = ['username', 'password']

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'comm-text-form'}),
        }


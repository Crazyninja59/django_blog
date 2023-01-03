from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth import logout, login

from .models import *
from .forms import *


# Create your views here.


class HomeView(ListView):
    model = Post
    template_name = 'blogapp/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['categories'] = Category.objects.all()
        return context


def category_view(request, slug):
    categories = Category.objects.all()
    posts = Post.objects.filter(category__slug=slug)
    return render(request, 'blogapp/index.html', {'title': f'Страница категории {Category.objects.get(slug=slug).name}', 'posts': posts, 'categories': categories})


class DetailView(DetailView):
    model = Post
    template_name = 'blogapp/post.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['comments'] = Comment.objects.filter(post_id=context['post'].pk)
        liked = False
        if context['post'].likes.filter(pk = self.request.user.pk).exists():
            liked = True
        context['liked'] = liked
        context['likes'] = context['post'].likes.count()

        return context



def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


def add_post(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                post = form.save(commit=False)
                post.author = request.user
                form.save()
                return redirect('home')
            except:
                form.add_error(None, "Форма не валидна")
    else:
        form = AddPostForm()
    return render(request, 'blogapp/add_post.html', {'form' : form, 'title': 'Добавление записи'})

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'blogapp/register.html'
    success_url = reverse_lazy('home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация пользователя'
        return context
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'blogapp/login.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация пользователя'
        return context

    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('home')

def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)

def like_view(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(pk = request.user.pk).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', pk=post.pk)
from django.urls import path
from .views import *
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<int:pk>', DetailView.as_view(), name="post_detail"),
    path('add_post', add_post, name='add_post'),
    path('cat/<slug:slug>', category_view, name="category_view"),
    path('register/', RegisterUser.as_view(), name="register"),
    path('login/', LoginUser.as_view(), name="login"),
    path('logout', logout_user, name="logout"),
    path('comment/<int:pk>', add_comment, name="add_comment"),
    path('like/<int:pk>', like_view, name="like_post")

]
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    objects = models.Manager()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    content = models.TextField(verbose_name='Описание статьи', null=True)
    image = models.FileField(upload_to='images/', verbose_name='Вставить изображение')
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовать')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Категория')
    likes = models.ManyToManyField(User, related_name='blog_post', verbose_name='Лайки')
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name="Пост")
    text = models.TextField(verbose_name="Содержимое")
    objects = models.Manager()
    def __str__(self):
        return f"Комментарий {self.author} для поста {self.post}"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


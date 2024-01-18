import datetime

from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User


def user_post_upload_to(instance, filename):
    user_slug = instance.slug
    current_time = datetime.datetime.now()
    filename = f'{current_time}_{filename}'
    return f'posts/{user_slug}/{filename}'


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=False, verbose_name="content")
    photo = models.ImageField(upload_to=user_post_upload_to, verbose_name="photo")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    time_update = models.DateTimeField(auto_now=True, verbose_name="update time")
    is_published = models.BooleanField(default=True)
    like = models.IntegerField(verbose_name='Likes number', null=True)
    dislike = models.IntegerField(verbose_name='Dislikes number', null=True, blank=True)
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name="categories")  # Foreign key (category)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user")

    def like_post(self, flag):
        if flag:
            self.like += 1
        else:
            self.like -= 1
        self.save()

    def dislike_post(self, flag):
        if flag:
            self.dislike += 1
        else:
            self.dislike -= 1
        self.save()

    def get_absolute_url(self):
        return reverse('main:post_detail', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Publication'
        ordering = ['-time_create', 'title']


class EvaluationController(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user")
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name="post")
    evaluation = models.CharField(max_length=255,
                                  choices=[('like', 'Like'), ('dislike', 'Dislike'), ('zero', 'Zero')],
                                  default=('zero', 'Zero'))

    def __str__(self):
        return f"{self.user}-{self.post_id}-{self.evaluation}"


class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="user")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name="post")

    class Meta:
        verbose_name = 'Comment'
        ordering = ['created_time']

    def __str__(self):
        return f'{self.user}-{self.pk}-{self.created_time}'


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name="category")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def get_absolute_url(self):
        return reverse('main:category', kwargs={'cat_slug': self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['id']


class Search(models.Model):
    name = models.CharField(max_length=60, verbose_name='Branch name')
    lng = models.FloatField(verbose_name='Longitude')
    lat = models.FloatField(verbose_name='Latitude')
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True, verbose_name='Status')

    def __str__(self):
        return self.name

from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=False, verbose_name="content")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="photo")
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
            self.like += 1
        self.save()

    def dislike_post(self, flag):
        if flag:
            self.like += 1
        else:
            self.like += 1
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
                                  choices=[('like', 'Like'), ('dislike', 'Dislike')],
                                  default=None)

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
        return f'{self.user}-{self.post_id}-{self.created_time}'


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

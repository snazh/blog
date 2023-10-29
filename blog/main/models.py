from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="title")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=False, verbose_name="content")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="photo")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="create time")
    time_update = models.DateTimeField(auto_now=True, verbose_name="update time")
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="categories")  # Foreign key (category)

    def get_absolute_url(self):
        return reverse('main:post_detail', kwargs={'post_slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:  # displaying manner
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'
        ordering = ['-time_create', 'title']


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

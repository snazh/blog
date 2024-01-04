from django.db import models
from django.contrib.auth.models import User
import datetime
from django.urls import reverse


def user_avatar_upload_to(instance, filename):

    user_slug = instance.slug
    current_time = datetime.datetime.now()
    filename = f'{current_time}_{filename}'
    return f'avatars/{user_slug}/{filename}'


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, verbose_name='URL', db_index=True, max_length=255)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30,null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_upload_to, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('users:user_profile', kwargs={'user_slug': self.slug})


from django.contrib import admin
from django.contrib.auth.models import User

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'slug', 'bio', 'avatar']
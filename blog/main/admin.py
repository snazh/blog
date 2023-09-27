from django.contrib import admin
from .models import *
from django.contrib import admin


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published')
    list_display_link = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('time_create', 'is_published')
    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_link = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)

from django.contrib import admin
from .models import *
from django.contrib import admin


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'slug', 'title', 'time_create', 'photo', 'is_published', 'like', 'dislike')
    list_display_link = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published','like','dislike')
    list_filter = ('time_create', 'is_published')
    prepopulated_fields = {"slug": ("title",)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_link = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_time')


class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'evaluation')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(EvaluationController, EvaluationAdmin)

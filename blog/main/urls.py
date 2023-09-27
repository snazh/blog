from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', index, name='home'),
                  path('about/', about, name='about'),
                  path('contacts/', contacts, name='contacts'),
                  path('login/', login, name='login'),
                  path('registration/', RegisterUser.as_view(), name='registration'),
                  path('posts/', MainPosts.as_view(), name='posts'),
                  path('add_post/', AddPost.as_view(), name='add_post'),
                  path('post_detail/<slug:post_slug>/', ShowPost.as_view(), name='post_detail'),
                  path('category/<slug:cat_slug>/', MainCategory.as_view(), name='category'),

              ]

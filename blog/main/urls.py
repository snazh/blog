from django.urls import path
from .views import *

app_name = 'main'
urlpatterns = [
    path('', index, name='home'),
    path('about/', about, name='about'),

    path('posts/', MainPosts.as_view(), name='posts'),
    path('add_post/', AddPost.as_view(), name='add_post'),
    path('post_detail/<slug:post_slug>/', ShowPost.as_view(), name='post_detail'),
    path('category/<slug:cat_slug>/', MainCategory.as_view(), name='category'),
    path('post_detail/<slug:post_slug>/add_comment/', AddCommentView.as_view(), name='add_comment'),
    path('contacts/', map_view, name='contacts')
]

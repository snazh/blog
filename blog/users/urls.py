from django.urls import path
from .views import *



app_name = 'users'
urlpatterns = [

    path('register/', SignUp.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('user_profile/<slug:user_slug>/', ShowUser.as_view(), name='user_profile'),
    path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),

]
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('user_profile/', views.User_Profile, name='user_profile'),
]

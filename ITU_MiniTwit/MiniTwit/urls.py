from django.urls import path
from .views import *

app_name = 'crm'

urlpatterns = [
    path('', timeline, name="timeline"),
    path('public/', public_timeline, name="public-timeline"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('register/', register, name="register"),
    path('addmessage/', add_message, name="add-message"),
    path('<str:pk>/', user_profile_timeline, name="user-profile-timeline"),
    path('<str:pk>/follow', follow_user, name="follow-user"),
    path('<str:pk>/unfollow', unfollow_user, name="unfollow-user"),
]
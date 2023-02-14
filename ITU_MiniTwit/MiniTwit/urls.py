from django.urls import path
from .views import *

app_name = 'crm'

urlpatterns = [
    path('', timeline, name="timeline"),
    path('login/', login, name="login"),
    path('logout/', logout, name="logout"),
    path('addmessage/', add_message, name="add-message"),
    path('<str:pk>/', user_timeline, name="user-timeline"),
    path('<str:pk>/follow', follow_user, name="follow-user"),
    path('<str:pk>/unfollow', unfollow_user, name="unfollow-user"),
]
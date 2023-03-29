from django.urls import include, path
from .views import *

app_name = 'crm'

urlpatterns = [
    path('', timeline, name="timeline"),
    path('public/', public_timeline, name="public-timeline"),
    path('login/', index_login, name="login"),
    path('logout/', index_logout, name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('addmessage/', add_message, name="add-message"),
    path('<str:pk>/', user_profile_timeline, name="user-profile-timeline"),
    path('<str:pk>/follow', follow_user, name="follow-user"),
    path('<str:pk>/unfollow', unfollow_user, name="unfollow-user"),
]
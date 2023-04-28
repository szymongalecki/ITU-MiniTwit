from django.urls import path
from django.views.generic.base import RedirectView
from .views import SignUpView, add_message, user_profile_timeline, follow_user, unfollow_user
from .views import timeline, public_timeline, index_login, index_logout

app_name = "minitwit"

urlpatterns = [
    path('', timeline, name="timeline"),
    path("favicon.ico/",
         RedirectView.as_view(url='/static/favicon.ico', permanent=True), name="favicon.ico"),
    path('public/', public_timeline, name="public-timeline"),
    path('login/', index_login, name="login"),
    path('logout/', index_logout, name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('addmessage/', add_message, name="add-message"),
    path('<str:pk>/', user_profile_timeline, name="user-profile-timeline"),
    path('<str:pk>/follow', follow_user, name="follow-user"),
    path('<str:pk>/unfollow', unfollow_user, name="unfollow-user")
]

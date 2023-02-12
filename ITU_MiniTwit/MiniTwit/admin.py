from django.contrib import admin
from .models import Follower, User, Message

admin.site.register(Follower)
admin.site.register(User)
admin.site.register(Message)

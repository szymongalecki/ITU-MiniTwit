from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(unique=True, null=False)


class Follower(models.Model):
    who_id = models.ForeignKey(User, related_name="who_id", on_delete=models.CASCADE, null=True)
    whom_id = models.ForeignKey(User, related_name="whom_id", on_delete=models.CASCADE, null=True)


class Message(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=280, null=False)
    pub_date = models.DateTimeField(auto_now_add=True)
    flagged = models.BooleanField(default=False)

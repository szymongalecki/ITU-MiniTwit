# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(unique=True, null=False)
    
    class Meta:
        db_table = 'user'

class Follower(models.Model):
    who = models.ForeignKey(User, related_name='who', on_delete=models.CASCADE, null=True)
    whom = models.ForeignKey(User, related_name='whom', on_delete=models.CASCADE, null=True)
    
    class Meta:
        db_table = 'follower'

class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=280, null=False)
    pub_date = models.DateTimeField(null=False)
    flagged = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'message'

class MigrateMessages(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=280, null=False)
    pub_date = models.DateTimeField(null=False)
    flagged = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'migrateMessages'

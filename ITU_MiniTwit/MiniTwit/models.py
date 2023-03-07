# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser


class Follower(models.Model):
    who_id = models.IntegerField(blank=True, null=True)
    whom_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'follower'


class Message(models.Model):
    message_id = models.AutoField(primary_key=True, blank=True, null=False)
    author_id = models.IntegerField()
    text = models.TextField()  # This field type is a guess.
    pub_date = models.IntegerField(blank=True, null=True)
    flagged = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'message'


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True, blank=True, null=False)
    username = models.TextField(max_length=50, unique=True, null=False)  # This field type is a guess.
    email = models.TextField(unique=True, null=False)  # This field type is a guess.
    password = models.CharField(db_column='pw_hash', max_length=128)   # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'user'

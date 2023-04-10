from django.db import models
from django.contrib.postgres.fields import ArrayField

class Message(models.Model):
    token = models.IntegerField()
    question = models.TextField()
    isKazakh = models.BooleanField()
    answer = models.TextField(null=True)
    conv_id = models.TextField(null=True)

class Person(models.Model):
    user_c = models.IntegerField()
    email = models.TextField()
    password = models.TextField()

class Conversations(models.Model):
    conv_id= models.TextField()
    title = models.TextField()
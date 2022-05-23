import datetime

from django.contrib.postgres.fields import ArrayField
from django.db import models

class Person(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=255)
    followed = ArrayField( models.IntegerField() ) # LFU ids

    def __str__(self):
        return f'Username: {self.username}, password: {self.password}'

class Post(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=1024)
    # createdBy = models.ForeignKey(Person, on_delete=models.CASCADE)

class Feedback(models.Model):
    email = models.CharField(max_length=50)
    text = models.CharField(max_length=1024)

class Reply(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)
    created_at = models.DateTimeField(null=False)


class LookingForYou(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    text = models.CharField(max_length=1024)
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(null=False)
    replies = ArrayField(models.IntegerField(), null=True)

class Notification(models.Model):
    lfu = models.ForeignKey(LookingForYou, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

class History(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
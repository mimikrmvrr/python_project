from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True)
    location = models.CharField(max_length=100, blank=True)
    start_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(blank=True)
    creator = models.ForeignKey(User, related_name='created_events')
    people = models.ManyToManyField(User, related_name='events')
    groups = models.ManyToManyField(Group, related_name='events')


class Comment(models.Model):
    text = models.TextField(max_length=200)
    created = models.DateTimeField(default=datetime.now)
    creator = models.ForeignKey(User, related_name='comments')
    event = models.ForeignKey(Event, related_name='comments')


# class MyTime(models.Model):
#     time = models.TimeField()
#     date = models.DateField()
#     datetime = models.DateTimeField()
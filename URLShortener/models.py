from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class RandomUsers(User):
    def __unicode__(self):
        return self.username

class UserURLS(models.Model):
    user_url = models.URLField(max_length = 600)
    short_url = models.CharField(max_length = 100)
    user = models.ForeignKey('RandomUsers', on_delete=models.CASCADE)

    def __unicode__(self):
        return self.user_url


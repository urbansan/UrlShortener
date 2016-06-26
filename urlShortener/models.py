from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from random import randint


class random_users(User):


    def __unicode__(self):
        return self.username

class user_urls(models.Model):
      
    user_url = models.URLField(max_length = 600)
    short_url = models.URLField(max_length = 100)
    user = models.ForeignKey(
        'random_users',
        on_delete=models.CASCADE
    )

    def __unicode__(self):
        return self.user_url


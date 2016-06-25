from __future__ import unicode_literals

from django.db import models

from django.db.models.aggregates import Count
from random import randint


class random_users(models.Model):
    user_name = models.CharField(max_length = 20)
    first_name = models.CharField(max_length = 20)
    last_name = models.CharField(max_length = 20)
    email = models.EmailField()
    password = models.CharField(max_length = 20)
    date_joined = models.DateTimeField(auto_now_add = True, auto_now = False)

    def __unicode__(self):
        return 'randomUser: ' + self.user_name

# def get_random_user_pk():

#     i = randint(0, random_users().objects.count() - 1)
#     user = random_users().objects.all()[i]
#     return user._meta.pk.name

class user_urls(models.Model):
      
    user_url = models.URLField(max_length = 600)
    short_url = models.URLField(max_length = 100)
    user = models.ForeignKey(
        'random_users',
        on_delete=models.CASCADE
        # default = randint(101, 200)
        # default = random_users.objects.all()[randint(0, random_users.objects.count() -1)].id 
    )

    def __unicode__(self):
        return self.user_url


from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.validators import URLValidator
from backend import randomusersAPI
from .forms import userUrlForm
from .models import random_users, user_urls
from random import randint
from uuid import uuid4
import pdb

SHORT_URL_MAX_LEN = 10

def getUniqueId():
    shortUrl = str(uuid4()).replace('-', '')[:SHORT_URL_MAX_LEN]
    try:
        user_urls.objects.get(short_url = shortUrl)
        getUniqueId()
    except:
        return shortUrl

def index(request):
    context = {}
    form = userUrlForm(request.POST or None)

    if form.is_valid():
        validate = URLValidator()
        try:
            userUrl = form.data['user_url'] 
            validate(userUrl)

            obtainedRecord, isCreated = user_urls.objects.get_or_create(
                user_url = userUrl,
                defaults={
                    'user': random_users.objects.all()[randint(0, random_users.objects.count() -1)],
                    'short_url' : getUniqueId()
                 }
            )

            return HttpResponseRedirect('/!' + obtainedRecord.short_url)

        except ValidationError, e:

            print e
            context.update({'errors' : e})

    context.update({'form' : form})
    return render(request, 'home.html', context)

def short(request, shortUrl = None):
    record = user_urls.objects.get(short_url = shortUrl)
    context = {'record' : record}
    return render(request, 'short.html', context)

def redirect(request, shortUrl):
    record = user_urls.objects.get(short_url = shortUrl)
    return HttpResponseRedirect(record.user_url)

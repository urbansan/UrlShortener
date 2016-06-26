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

SHORT_URL_MAX_LEN = 0

def getUniqueId(recursion_depth):

    if recursion_depth > 50:
        pass

    shortUrl = str(uuid4()).replace('-', '')[:SHORT_URL_MAX_LEN]
    try:
        user_urls.objects.get(short_url = shortUrl)
        print recursion_depth
        recursion_depth += 1
        getUniqueId(recursion_depth)
 
    except:
        print 'wlezlimy tu'
        return shortUrl

    return '-1'

def index(request):
    context = {}
    form = userUrlForm(request.POST or None)

    if form.is_valid():
        validate = URLValidator()
        try:
            userUrl = form.data['user_url'] 
            validate(userUrl)

            shortUrl = getUniqueId(1)
            if cmp(shortUrl, '-1') == 0:
                raise ValidationError('The pool of unique short URLs has been used')


            # Check if DB is empty. Throws ValueError on none records in DB.
            random_user_instance = random_users.objects.all()[randint(0, random_users.objects.count() -1)]

            obtainedRecord, isCreated = user_urls.objects.get_or_create(
                user_url = userUrl,
                defaults={
                    'user': random_user_instance,
                    'short_url' : shortUrl
                 }
            )

            return HttpResponseRedirect('/!' + obtainedRecord.short_url)

        except ValidationError, e:
            print e
            context.update({'errors' : e})
        except ValueError:
            context.update({'errors' : ['Please populate the DB with random users']})

    context.update({'form' : form})
    return render(request, 'urlShortener/home.html', context)

def short(request, shortUrl = None):
    record = user_urls.objects.get(short_url = shortUrl)
    context = {'record' : record, 'host' : request.META['HTTP_HOST']}
    return render(request, 'urlShortener/short.html', context)

def redirect(request, shortUrl):
    record = user_urls.objects.get(short_url = shortUrl)
    return HttpResponseRedirect(record.user_url)

def about(request):
    return render(request, 'urlShortener/about.html')

def contact(request):
    return render(request, 'urlShortener/contact.html')
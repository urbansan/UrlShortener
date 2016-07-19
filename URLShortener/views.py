from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.validators import URLValidator
from .forms import UserURLForm
from .models import RandomUsers, UserURLS
from random import randint
from uuid import uuid4
import pdb

SHORT_URL_MAX_LEN = 10

def get_unique_id(recursion_depth):

    if recursion_depth > 50:
        return '-1'

    shortUrl = str(uuid4()).replace('-', '')[:SHORT_URL_MAX_LEN]
    cursor = UserURLS.objects.filter(short_url = shortUrl)

    if len(cursor):
        recursion_depth += 1
        return get_unique_id(recursion_depth)
 
    return shortUrl

def index(request):
    context = {}
    form = UserURLForm(request.POST or None)
    context.update({'form' : form})

    if form.is_valid():
        # context.update({'form' : form})
        userUrl = form.data['user_url'] 

        shortUrl = get_unique_id(1)
        if shortUrl == '-1':
            context.update({'errors' : ['The pool of unique short URLs has been used']})
            return render(request, 'URLShortener/home.html', context)

        all_random_users = RandomUsers.objects.all()
        if not all_random_users:
            context.update({'errors' : ['Please populate the DB with random users']})
            return render(request, 'URLShortener/home.html', context)

        random_user_instance = all_random_users[randint(0, len(all_random_users) - 1)]
        obtained_record, isCreated = UserURLS.objects.get_or_create(
            user_url = userUrl,
            defaults={
                'user': random_user_instance,
                'short_url' : shortUrl
             }
        )
        return HttpResponseRedirect('/!' + obtained_record.short_url)
    # else:
    #     context.update({'errors' : ['Invalid form']})
    #     return render(request, 'URLShortener/home.html', context)

    context.update({'form' : form})
    return render(request, 'URLShortener/home.html', context)

def short(request, shortUrl = None):
    record = UserURLS.objects.get(short_url = shortUrl)
    context = {'record' : record, 'host' : request.META['HTTP_HOST']}
    return render(request, 'URLShortener/short.html', context)

def redirect(request, shortUrl):
    record = UserURLS.objects.get(short_url = shortUrl)
    return HttpResponseRedirect(record.user_url)

def about(request):
    return render(request, 'URLShortener/about.html')

def contact(request):
    return render(request, 'URLShortener/contact.html')
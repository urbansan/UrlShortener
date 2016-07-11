from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.validators import URLValidator
from .forms import UserURLForm
from .models import RandomUsers, UserURLS
from random import randint
from uuid import uuid4

SHORT_URL_MAX_LEN = 10

def get_unique_id(recursion_depth):

    if recursion_depth > 50:
        pass

    shortUrl = str(uuid4()).replace('-', '')[:SHORT_URL_MAX_LEN]
    try:
        UserURLS.objects.get(short_url = shortUrl)

        recursion_depth += 1
        get_unique_id(recursion_depth)
 
    except:
        return shortUrl

    return '-1'

def index(request):
    context = {}
    form = UserURLForm(request.POST or None)

    if form.is_valid():
        validate = URLValidator()
        try:
            userUrl = form.data['user_url'] 
            validate(userUrl)

            shortUrl = get_unique_id(1)
            if cmp(shortUrl, '-1') == 0:
                raise ValidationError('The pool of unique short URLs has been used')

            # Check if DB is empty. Throws ValueError on none records in DB.
            random_user_instance = RandomUsers.objects.all()[randint(0, RandomUsers.objects.count() -1)]

            obtainedRecord, isCreated = UserURLS.objects.get_or_create(
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
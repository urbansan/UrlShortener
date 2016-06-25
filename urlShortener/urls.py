from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about$', views.about, name='about'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^!(?P<shortUrl>.*)$', views.short, name='short'),
    url(r'^(?P<shortUrl>.*)$', views.redirect, name='redirect'),
]    
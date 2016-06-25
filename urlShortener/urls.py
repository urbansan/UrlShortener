from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^short$', views.short, name='short'),
    url(r'^!(?P<shortUrl>.*)$', views.short, name='short'),
    url(r'^(?P<shortUrl>.*)$', views.redirect, name='redirect'),
]    
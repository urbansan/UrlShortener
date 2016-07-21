from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from URLShortener.models import UserURLS, RandomUsers


class UserURLSResource(ModelResource):
    class Meta:
        queryset = UserURLS.objects.all()
        allowed_methods = ['get']
        serializer = Serializer(formats=['json'])

class RandomUsersResource(ModelResource):
    class Meta:
        queryset = RandomUsers.objects.all()
        allowed_methods = ['get']
        serializer = Serializer(formats=['json'])
        excludes = ['password', 'date_joined', 'is_superuser', 'id', 'is_active']

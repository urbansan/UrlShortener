from django.forms import ModelForm, TextInput
from .models import user_urls
from django.utils.translation import ugettext_lazy as _

class userUrlForm(ModelForm):
    class Meta:
        model = user_urls
        fields = ['user_url']
        widgets = {
            # 'class': 'form-control',
            'user_url': TextInput(attrs={'placeholder' : 'Url...', 'class': 'form-control'}),
            # 'placeholder' : 'Url...'
        }
        labels = {
            'user_url' : 'Submit an URL to shorten it'

        }


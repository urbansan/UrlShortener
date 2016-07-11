from django.forms import ModelForm, TextInput
from .models import UserURLS
# from django.utils.translation import ugettext_lazy as _

class UserURLForm(ModelForm):
    class Meta:
        model = UserURLS
        fields = ['user_url']
        widgets = {
            # 'class': 'form-control',
            'user_url': TextInput(attrs={'placeholder' : 'Url...', 'class': 'form-control'}),
            # 'placeholder' : 'Url...'
        }
        labels = {
            'user_url' : ''

        }


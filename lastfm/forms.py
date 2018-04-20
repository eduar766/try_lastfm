from django.forms import ModelForm, TextInput
from .models import Country

class CountryForm(ModelForm):
    class Meta:
        model = Country
        fields = ['name']
        widgets = {
            'name': TextInput(
                attrs = {
                    'placeholder': 'Search by Country...'
                }
            )
        }

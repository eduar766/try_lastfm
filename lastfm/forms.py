from django.forms import ModelForm, TextInput
from .models import Country, Artist

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


class ArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = ['name']
        widgets = {
            'name': TextInput(
                attrs = {
                    'placeholder': 'Search Artist...'
                }
            )
        }

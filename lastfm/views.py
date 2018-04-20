from django.shortcuts import render, redirect
import requests
from lastfm.models import Country, Artist
from .forms import CountryForm, ArtistForm

# Create your views here.
def index(request):
    url = 'http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists&country={}&api_key={}&format=json'
    token = '1bd4499f020556b281c2a605cfa2cb23'
    countrys = Country.objects.all()

    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            p = request.POST.get('name')
            c = Country.objects.get(pk=1)
            c.name = p
            c.save()

    form = CountryForm()

    artist_collect = []

    for country in countrys:
        r = requests.get(url.format(country, token)).json()
        i = 0

        while i < 10:
            artist_attrs = {
                'name': r['topartists']['artist'][i]['name'],
                'link': r['topartists']['artist'][i]['url'],
                'photo': r['topartists']['artist'][i]['image'][2]['#text']
            }
            artist_collect.append(artist_attrs)
            i = i + 1

    context = {'artist_collect': artist_collect, 'country': country, 'form':form}

    return render(request, 'lastfm/index.html', context)


def artist(request):
    url = 'http://ws.audioscrobbler.com/2.0/?method=artist.getinfo&artist={}&api_key={}&format=json'
    token = '1bd4499f020556b281c2a605cfa2cb23'
    artists = Artist.objects.all()


    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid:
            p = request.POST.get('name')
            a = Artist.objects.get(pk=1)
            a.name = p
            a.save()

    form = ArtistForm()

    for artist in artists:
        r = requests.get(url.format(artist, token)).json()
        artist_collect = []

        artist_attrs = {
            'name': r['artist']['name'],
            'link': r['artist']['url'],
            'photo': r['artist']['image'][3]['#text'],
            'listeners': r['artist']['stats']['listeners'],
            'playcount': r['artist']['stats']['playcount'],
            'bio': r['artist']['bio']['summary'],
        }
        artist_collect.append(artist_attrs)

        artist_related_collect = []
        i = 0
        while i < 4:
            artist_related = {
                'related': r['artist']['similar']['artist'][i]['name'],
                'related_link': r['artist']['similar']['artist'][i]['url'],
                'related_img': r['artist']['similar']['artist'][i]['image'][2]['#text']
            }

            artist_related_collect.append(artist_related)
            i = i + 1

    context = {'artist_collect': artist_collect,
                'artist_related_collect': artist_related_collect,
                'form': form}

    return render(request, 'lastfm/artist.html', context)

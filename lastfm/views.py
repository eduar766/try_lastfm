from django.shortcuts import render, redirect
import requests
from .models import Country
from .forms import CountryForm

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


# def search_country(request, id):
#     form = CountryForm(request.POST)
#
#     if form.is_valid():
#         new_form = form.save()
#
#     # p = Country.objects.get(pk=1)
#     # p.name = id.name
#     print(id)
#
#     return redirect('index')

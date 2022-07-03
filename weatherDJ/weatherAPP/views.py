from django.shortcuts import render
import requests

from . import config
from .models import City
from .forms import CityForm


def index(request):
    apikey = config.APIKEY
    # insert your api key from https://openweathermap.org/api

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()
    elif request.method == 'GET':
        QueryDict = request.GET.fromkeys(request.GET, value='Удалить')
        if QueryDict:
            name = list(QueryDict.keys())[1]
            City.objects.filter(name=name).delete()

    form = CityForm()

    cities = City.objects.all()
    all_cities = []

    for city in cities:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={apikey}'
        res = requests.get(url).json()
        city_info = {
            'city': city.name,
            'temp': res['main']['temp'],
            'icon': res['weather'][0]['icon'],
        }
        all_cities.append(city_info)

    context = {'all_info': all_cities,
               'form': form}

    return render(request, 'weatherAPP/index.html', context)


def temp(request):
    return render(request, 'weatherAPP/temp.html')

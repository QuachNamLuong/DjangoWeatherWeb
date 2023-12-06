from django.forms import ValidationError
from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
import json

def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=0576e071c691c65048556b66ee22d479&lang=vi"
    
    if request.method == 'POST':
        name = request.POST.get('name')
        city_weather = requests.get(url.format(name)).json()
        form = CityForm(request.POST)
        if city_weather['cod'] == 200:
            form.save()


    form = CityForm()
    cities = City.objects.all()
    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city)).json()
        if city_weather['cod'] == 200:
            weather = {
                    'city' : city_weather['name'],
                    'temperature' : city_weather['main']['temp'],
                    'description' : city_weather['weather'][0]['description'],
                    'icon' : city_weather['weather'][0]['icon']
                }
            weather['temperature'] = round((weather['temperature'] - 32) / (9/5))
            weather_data.append(weather)
        else:
            City.objects.filter(name=city).delete()

    context = {'weather_data' : weather_data, 'form' : form}

    return render(request, 'weather/index.html', context)


from .scripts import find_timezone, forming_location_dict, get_coordinates
from django.shortcuts import render
from rest_framework import generics
from django.db.models import F
from django.views import View
from . import serializers
import translators as ts
from .models import City
import requests
class WeatherListView(View):
    def get(self, request):
        # user_city_from_ip = get_city_from_ip(request)
        try:
            lat = request.COOKIES['search_history_latitude']
            lon = request.COOKIES['search_history_longitude']
            name = request.COOKIES['search_history_name']
            request_to_api_weather = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature').json()
            print(f'request_to_api_weather === {request_to_api_weather}')

            timezone = find_timezone(float(lat), float(lon))
            request_to_api_utc = requests.get(f'http://worldtimeapi.org/api/timezone/{timezone}').json()
            location_dict = {
                'name': name, 
                'lat': lat, 
                'lon': lon
            }
            location_dict = forming_location_dict(request, request_to_api_weather, location_dict)
            response = render(request, "search.html", location_dict)
        except Exception as Exp:
            response = render(request, "search.html", {'response':[]})

        return response
    def post(self, request):
        city_from_search = request.POST.get('search')
        location_dict = get_coordinates(f'{city_from_search}')
        if (location_dict):

            request_to_api_weather = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={location_dict["lat"]}&longitude={location_dict["lon"]}&current=temperature').json()
            
            if City.objects.filter(city=location_dict['name']).exists():
                print("Запись существует")
                City.objects.filter(city=location_dict['name']).update(count = F('count') + 1)
            else:
                print("Записи не существует")
                save_city_search = City(city = city_from_search, latitude = location_dict["lat"], longitude = location_dict["lon"])
                save_city_search.save()
                
            location_dict = forming_location_dict(request, request_to_api_weather, location_dict)
            response = render(request, "city.html", location_dict)
            
            response.set_cookie('search_history_name', ts.translate_text(location_dict["name"]))
            response.set_cookie('search_history_latitude', location_dict["lat"])
            response.set_cookie('search_history_longitude', location_dict["lon"])

            return response
        else:
            response = render(request, "city.html", {'name': "Простите, мы не смогли найти введенный вами город, возможно в названии была совершена ошибка. Попробуйте еще раз"})
            return response

class CityList(generics.ListAPIView):
    queryset = City.objects.all().order_by('-count')
    serializer_class = serializers.CitySearchSerializer

from timezonefinder import TimezoneFinder 
from geopy.geocoders import Nominatim
# from geoip2 import database
import requests
import os
import re

from .models import City

def find_timezone(latitude, longitude):     
    return TimezoneFinder().timezone_at(lng = longitude, lat = latitude)

def get_coordinates(city_name):
     try:
        app = Nominatim(user_agent="tutorial")
        location = (app.geocode(city_name).raw)
        print(f'location === {location}')
        return {
            'name': location['name'], 
            'display_name': location['display_name'], 
            'lat': location['lat'], 
            'lon': location['lon']
        }
     except Exception as Exp:
         print(Exp)
         return None

# def get_city_from_ip(request):
#     """
#     Функция, которая определяет город пользователя по его IP-адресу.
#     Args:
#         request (django.http.request.HttpRequest): Объект запроса Django.
#     Returns:
#         str: Название города на английском языке, если он был определен успешно.
#              В случае ошибки возвращает `None`.
#     """
#     # Формируем путь к базе данных, которая содержит информацию о расположении IP-адресов
#     geoip_database_path = os.path.join(os.path.dirname(__file__), 'GeoLite2-City.mmdb')
#     print(f" Путь к БД -> {geoip_database_path}")
#     try:
#         # Открываем базу данных с помощью класса Reader из библиотеки geoip2.database
#         with database.Reader(geoip_database_path) as reader:
#             # Получаем информацию о городе по IP-адресу пользователя
#             response = reader.city(request.META['REMOTE_ADDR'])
#             # Получаем название города 
#             city = response.city.names['en']
#             return city
#     except Exception as Exp:
#         print(Exp)
#         return None



def forming_location_dict(request, request_to_api_weather, location_dict):
    location_dict['temperature'] = request_to_api_weather['current']['temperature']
    location_dict['time'] = request_to_api_weather['current']['time']

    timezone = find_timezone(float(location_dict['lat']), float(location_dict['lon']))
    request_to_api_utc = requests.get(f'http://worldtimeapi.org/api/timezone/{timezone}').json()

    match = re.match(r"([+-])(\d\d):(\d\d)", request_to_api_utc['utc_offset'])
    location_dict['UTC'] = request_to_api_utc['utc_offset']
    location_dict['UTC_delimiter'] = match.group(1)
    location_dict['UTC_hours'] = int(match.group(2))
    location_dict['UTC_minutes'] = int(match.group(3))

    location_dict['cities'] = City.objects.all()

    return location_dict
    
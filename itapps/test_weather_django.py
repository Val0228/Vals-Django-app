import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itapps.settings')
os.environ['OPENWEATHER_API_KEY'] = '4d046c5bfad41be3de5d9ec830b6f42e'
django.setup()

from django.conf import settings
from itreporting.services import WeatherService

print('API Key configured:', 'Yes' if settings.OPENWEATHER_API_KEY else 'No')
if settings.OPENWEATHER_API_KEY:
    print('API Key value:', settings.OPENWEATHER_API_KEY[:10] + '...')

ws = WeatherService()
weather = ws.get_weather_by_city('Sheffield', 'GB')

print('\nWeather Service Test:', 'SUCCESS' if weather else 'FAILED')
if weather:
    print('City:', weather.get('city'))
    print('Temperature:', weather.get('temperature'), 'C')
    print('Description:', weather.get('description'))
    print('Humidity:', weather.get('humidity'), '%')
    print('Wind Speed:', weather.get('wind_speed'), 'km/h')


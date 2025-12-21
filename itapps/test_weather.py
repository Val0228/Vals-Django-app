import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itapps.settings')
os.environ['OPENWEATHER_API_KEY'] = '4d046c5bfad41be3de5d9ec830b6f42e'
django.setup()

from itreporting.services import WeatherService

ws = WeatherService()
weather = ws.get_weather_by_city('Sheffield', 'GB')

if weather:
    print("Weather API Test: SUCCESS")
    print(f"City: {weather.get('city')}")
    print(f"Temperature: {weather.get('temperature')}C")
    print(f"Description: {weather.get('description')}")
    print(f"Humidity: {weather.get('humidity')}%")
    print(f"Wind Speed: {weather.get('wind_speed')} km/h")
else:
    print("Weather API Test: FAILED")
    print("Error: 401 Unauthorized")
    print("Possible reasons:")
    print("1. API key is invalid or not activated yet")
    print("2. API key needs time to activate (10-60 minutes)")
    print("3. Please verify the key at: https://home.openweathermap.org/api_keys")
    print("\nCurrent API Key:", os.environ.get('OPENWEATHER_API_KEY', 'Not set'))


"""
Weather API service for fetching weather data
"""
import requests
import os
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class WeatherService:
    """
    Service class for interacting with OpenWeatherMap API
    """
    
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    def __init__(self):
        self.api_key = os.environ.get('OPENWEATHER_API_KEY', '')
        if not self.api_key:
            logger.warning("OpenWeatherMap API key not found in environment variables")
    
    def get_weather_by_city(self, city_name="Sheffield", country_code="GB", units="metric"):
        """
        Get current weather by city name
        
        Args:
            city_name: Name of the city (default: Sheffield)
            country_code: Country code (default: GB for UK)
            units: Temperature units - metric (Celsius) or imperial (Fahrenheit)
        
        Returns:
            dict: Weather data or None if error
        """
        if not self.api_key:
            return None
        
        cache_key = f"weather_{city_name}_{country_code}_{units}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            url = f"{self.BASE_URL}/weather"
            params = {
                'q': f"{city_name},{country_code}",
                'APPID': self.api_key,
                'units': units
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Format the data for easier use in templates
            from datetime import datetime
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': round(data['wind']['speed'] * 3.6, 1),  # Convert m/s to km/h
                'pressure': data['main']['pressure'],
                'visibility': round(data.get('visibility', 0) / 1000, 1) if data.get('visibility') else None,
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']),
                'icon_url': f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
            }
            
            # Cache for 10 minutes
            cache.set(cache_key, weather_data, 600)
            
            return weather_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data: {str(e)}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"Error parsing weather data: {str(e)}")
            return None
    
    def get_weather_by_coords(self, lat, lon, units="metric"):
        """
        Get current weather by coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            units: Temperature units
        
        Returns:
            dict: Weather data or None if error
        """
        if not self.api_key:
            return None
        
        cache_key = f"weather_coords_{lat}_{lon}_{units}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            url = f"{self.BASE_URL}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'APPID': self.api_key,
                'units': units
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            from datetime import datetime
            weather_data = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon'],
                'humidity': data['main']['humidity'],
                'wind_speed': round(data['wind']['speed'] * 3.6, 1),
                'pressure': data['main']['pressure'],
                'visibility': round(data.get('visibility', 0) / 1000, 1) if data.get('visibility') else None,
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']),
                'icon_url': f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
            }
            
            cache.set(cache_key, weather_data, 600)
            
            return weather_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching weather data: {str(e)}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"Error parsing weather data: {str(e)}")
            return None
    
    def get_forecast(self, city_name="Sheffield", country_code="GB", days=5, units="metric"):
        """
        Get weather forecast for multiple days
        
        Args:
            city_name: Name of the city
            country_code: Country code
            days: Number of forecast days (max 5 for free tier)
            units: Temperature units
        
        Returns:
            dict: Forecast data or None if error
        """
        if not self.api_key:
            return None
        
        cache_key = f"forecast_{city_name}_{country_code}_{days}_{units}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            url = f"{self.BASE_URL}/forecast"
            params = {
                'q': f"{city_name},{country_code}",
                'APPID': self.api_key,
                'units': units,
                'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Process forecast data
            forecast_list = []
            for item in data['list'][:days * 8]:
                forecast_list.append({
                    'datetime': item['dt'],
                    'temperature': round(item['main']['temp']),
                    'description': item['weather'][0]['description'].title(),
                    'icon': item['weather'][0]['icon'],
                    'icon_url': f"https://openweathermap.org/img/wn/{item['weather'][0]['icon']}@2x.png",
                    'humidity': item['main']['humidity'],
                    'wind_speed': round(item['wind']['speed'] * 3.6, 1),
                })
            
            forecast_data = {
                'city': data['city']['name'],
                'country': data['city']['country'],
                'forecast': forecast_list
            }
            
            cache.set(cache_key, forecast_data, 600)
            
            return forecast_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching forecast data: {str(e)}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"Error parsing forecast data: {str(e)}")
            return None

#-------------------------------------------------------------------------------------------------

class NewsService:
    """
    Service class for interacting with The News API
    """
    
    BASE_URL = "api.thenewsapi.com"
    
    def __init__(self):
        self.api_token = os.environ.get('NEWS_API_TOKEN', '')
        if not self.api_token:
            logger.warning("The News API token not found in environment variables")
    
    def get_latest_news(self, categories='business,tech,sports', limit=3, locale='uk', language='en', source="www.bbc.co.uk" ):
        """
        Get latest news articles
        
        Args:
            categories: Comma-separated list of categories (default: business,tech,sports)
            limit: Number of articles to fetch (default: 3)
            locale: Locale code (default: uk)
            language: Language code (default: en)
            source: Source of the news (default: www.bbc.co.uk)
        
        Returns:
            list: List of news articles or empty list if error
        """
        if not self.api_token:
            return []
        
        cache_key = f"news_{categories}_{limit}_{locale}_{language}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            import http.client
            import urllib.parse
            
            conn = http.client.HTTPSConnection(self.BASE_URL)
            
            params = urllib.parse.urlencode({
                'api_token': self.api_token,
                'categories': categories,
                'limit': limit,
                'locale': locale,
                'language': language,
            })
            
            conn.request('GET', f'/v1/news/all?{params}')
            res = conn.getresponse()
            data = res.read()
            
            import json
            news_data = json.loads(data.decode('utf-8'))
            
            # Parse and format news articles
            articles = []
            if 'data' in news_data:
                for article in news_data['data'][:limit]:
                    articles.append({
                        'title': article.get('title', 'No title'),
                        'description': article.get('description', ''),
                        'url': article.get('url', '#'),
                        'source': article.get('source', 'Unknown'),
                        'published_at': article.get('published_at', ''),
                        'image_url': article.get('image_url', ''),
                        'snippet': article.get('snippet', '')[:150] + '...' if article.get('snippet') else '',
                    })
            
            # Cache for 15 minutes
            cache.set(cache_key, articles, 900)
            
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching news data: {str(e)}")
            return []


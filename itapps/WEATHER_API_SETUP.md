# Weather API Setup Guide

This guide will help you set up the OpenWeatherMap API integration for the campus weather feature.

## Step 1: Get an API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Click "Sign Up" to create a free account
3. After signing up, go to the [API Keys](https://home.openweathermap.org/api_keys) section
4. Generate a new API key (it may take a few minutes to activate)

## Step 2: Set Environment Variable

### For Local Development (Windows PowerShell):

```powershell
$env:OPENWEATHER_API_KEY="your_api_key_here"
```

### For Local Development (Windows CMD):

```cmd
set OPENWEATHER_API_KEY=your_api_key_here
```

### For Local Development (Linux/Mac):

```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

### For Permanent Setup (Windows):

1. Right-click "This PC" → Properties
2. Click "Advanced system settings"
3. Click "Environment Variables"
4. Under "User variables", click "New"
5. Variable name: `OPENWEATHER_API_KEY`
6. Variable value: Your API key
7. Click OK

### For Azure Deployment:

1. Go to your Azure App Service
2. Navigate to Configuration → Application settings
3. Click "+ New application setting"
4. Name: `OPENWEATHER_API_KEY`
5. Value: Your API key
6. Click OK and Save

## Step 3: Verify Setup

1. Start your Django server:
   ```bash
   python manage.py runserver
   ```

2. Visit the home page - you should see a weather widget
3. Visit `/itreporting/weather/` to see the full weather page

## Features

- **Current Weather**: Temperature, description, humidity, wind speed, pressure, visibility
- **5-Day Forecast**: Extended weather forecast
- **City Search**: Search weather for any city worldwide
- **Caching**: Weather data is cached for 10 minutes to reduce API calls
- **Error Handling**: Graceful fallback if API is unavailable

## API Limits (Free Tier)

- 60 calls per minute
- 1,000,000 calls per month
- Current weather data
- 5-day/3-hour forecast

## Troubleshooting

### Weather widget not showing:
- Check that `OPENWEATHER_API_KEY` is set correctly
- Verify the API key is active (may take a few minutes after creation)
- Check Django logs for error messages

### "Unable to fetch weather data":
- Verify your API key is correct
- Check your internet connection
- Ensure you haven't exceeded API rate limits
- Check that the city name and country code are correct

## Support

For API issues, visit [OpenWeatherMap Support](https://openweathermap.org/faq)


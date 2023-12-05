import openmeteo_requests
import requests_cache
from retry_requests import retry
from geopy.geocoders import Nominatim
import datetime


def weather(locate): 

    geolocator = Nominatim(user_agent="xaviercea")
    location =  geolocator.geocode(locate)

    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": location.latitude,
        "longitude": location.longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "pressure_msl", "surface_pressure"],
        "timezone": "GMT",
        "forecast_days": 1
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°E {response.Longitude()}°N")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Current values. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_apparent_temperature = current.Variables(2).Value()
    current_is_day = current.Variables(3).Value()
    current_pressure_msl = current.Variables(4).Value()
    current_surface_pressure = current.Variables(5).Value()

    print(f"Current time {datetime.datetime.fromtimestamp(current.Time())}")
    print(f"Current temperature_2m {round(current_temperature_2m, 2)}ºC")
    print(f"Current relative_humidity_2m {current_relative_humidity_2m}%")
    print(f"Current apparent_temperature {round(current_apparent_temperature, 2)}ºC")
    print(f"Current is_day {current_is_day}")
    print(f"Current pressure_msl {round(current_pressure_msl)} hPa")
    print(f"Current surface_pressure {round(current_surface_pressure)} hPa")
    
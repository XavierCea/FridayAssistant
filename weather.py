import openmeteo_requests
import requests_cache
from retry_requests import retry
from geopy.geocoders import Nominatim
import datetime


weather_codes = {
    0 : 'Despejado',
    1 : 'Principalmente despejado',
    2 : 'Parcialmente nublado',
    3 : 'Cubierto',
    45 : 'Niebla',
    48 : 'Niebla Escarchada',
    51 : 'Llovizna ligera',
    53 : 'Llovizna moderada',
    55 : 'Llovizna densa',
    56 : 'Llovizna helada ligera',
    57 : 'llovizna helada densa',
    61 : 'Lluvia leve',
    63 : 'Lluvia moderada',
    65 : 'LLuvia fuerte',
    66 : 'Lluvia helada ligera',
    67 : 'Lluvia helada fuerte',
    71 : 'Nevada leve',
    73 : 'Nevada moderada',
    75 : 'Nevada fuerte',
    77 : 'Granizo',
    80 : 'Lluvias leves',
    81 : 'Lluvias moderadas',
    82 : 'Lluvias violentas',
    85 : 'Chuvascos de nieve ligeros',
    86 : 'Chuvascos de nieve fuerte',
    95 : 'Tormenta leve o moderada',
    96 : 'Tormenta con granizo leve',
    99 : 'Tormenta con granizo fuerte'
}

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
        "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day", "weather_code", "pressure_msl", "surface_pressure"],
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
    current_weather_code = current.Variables(4).Value()
    current_pressure_msl = current.Variables(5).Value()
    current_surface_pressure = current.Variables(6).Value()
    current_weather = ''

    print(f"Current time {datetime.datetime.fromtimestamp(current.Time())}")
    print(f"Current temperature_2m {round(current_temperature_2m, 2)}ºC")
    print(f"Current relative_humidity_2m {current_relative_humidity_2m}%")
    print(f"Current apparent_temperature {round(current_apparent_temperature, 2)}ºC")
    print(f"Current is_day {current_is_day}")
    print(f"Current pressure_msl {round(current_pressure_msl)} hPa")
    print(f"Current surface_pressure {round(current_surface_pressure)} hPa")
    print(f"Current weather_code {current_weather_code}")
    
    for weather_code in weather_codes:
        if weather_code == current_weather_code:
            current_weather = weather_codes[weather_code]
    
    print(f'Current weather {current_weather}')
    
    return(f"La temperatura en {locate} es de {round(current_temperature_2m, 2)}," + 
           f" con una sensación térmica de {round(current_apparent_temperature, 2)}." + 
           f" el tiempo que tenemos es {current_weather}")
    
    
    
"This module contains the HourlyForecast class and the get_special_forecast method."

import requests

class HourlyForecast:
    "This class represents a single hourly forecast from the NWS API"
    def __init__(self, start_time, end_time, temperature, temperature_unit, wind_speed, \
        wind_direction, short_forecast, detailed_forecast):
        "Initialize the HourlyForecast class"
        self.start_time = start_time
        self.end_time = end_time
        self.temperature = temperature
        self.temperature_unit = temperature_unit
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        #self.wind_direction_compass = wind_direction_compass
        self.short_forecast = short_forecast
        self.detailed_forecast = detailed_forecast

class Forecast:
    "This class represents a single forecast from the NWS API"
    def get_special_forecast(self, latitude, longitude):
        "Get the special forecast from the NWS API"
        endpoint = "https://forecast.weather.gov/MapClick.php?w0=t&w1=td&w2=hi&w3=sfcwind&w3u=" \
            + "0&w4=sky&w5=pop&w6=rh&w7=rain&w8=thunder&pqpfhr=6&AheadHour=0&Submit=Submit&" \
            + "FcstType=json&textField1="
        endpoint += str(latitude)
        endpoint += "&textField2="
        endpoint += str(longitude)
        endpoint += "&site=all&unit=0&dd=&bw="
        # Make the API request with timeout set to 10 seconds
        response = requests.get(endpoint, timeout=30)

        # Check if the request was successful
        if response.status_code != 200:
            return None

        # Parse the JSON response
        return response.json()

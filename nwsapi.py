# Gathers weather data from NWS API and returns it as a JSON object
import requests
import nwsclass

class NWS(object):
    "This class represents the NWS API"
    lat = ''
    lng = ''
    json = ''
    def __init__(self, lat, lng):
        # get the latitude and longitude for the zip code
        self.lat = lat
        self.lng = lng

        # Set up the API endpoint and parameters
        endpoint = 'https://api.weather.gov/points/'

        # Make the API request with timeout set to 10 seconds
        response = requests.get(endpoint + self.lat + ',' + self.lng, timeout=10)
        
        # Parse the JSON response
        self.json = response.json()

        

    def get_current_weather(self):
        "Get the current weather from the NWS API"
        # Get the hourly forecast URL from the response
        forecast_hourly_url = self.json['properties']['forecastHourly']
        forecast_hourly_response = requests.get(forecast_hourly_url, timeout=10)
        forecast_hourly_data = forecast_hourly_response.json()
        # print the current weather
        current_data = forecast_hourly_data['properties']['periods'][0]
        start_time = current_data['startTime']
        end_time = current_data['endTime']
        temperature = current_data['temperature']
        temperature_unit = current_data['temperatureUnit']
        #temperature_trend = current_data['temperatureTrend']
        wind_speed = current_data['windSpeed']
        wind_direction = current_data['windDirection']
        #icon = current_data['icon']
        short_forecast = current_data['shortForecast']
        detailed_forecast = current_data['detailedForecast']
        currentWeather = nwsclass.HourlyForecast(start_time, end_time, temperature, temperature_unit, \
            wind_speed, wind_direction, short_forecast, detailed_forecast)
        return currentWeather

    def get_hourly_forecast(self):
        # Get the forecast URL from the response
        forecast_url = self.json['properties']['forecast']

        # Make another API request to the forecast URL with timeout set to 10 seconds
        forecast_response = requests.get(forecast_url, timeout=10)
        forecast_data = forecast_response.json()

        # print today's forecast
        print(forecast_data['properties']['periods'][0]['name'] + ': ' + forecast_data['properties']['periods'][0]['detailedForecast'])
        
        # loop through forecast data and print out the forecast for each day
        for forecast in forecast_data['properties']['periods']:
            # parse the forecast date time
            forecast_date = forecast['startTime'].split('T')[0]
            # print the forecast date and the forecast
            print(forecast_date + ': ' + forecast['name'] + ': ' + forecast['detailedForecast'])


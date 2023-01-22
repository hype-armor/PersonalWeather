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
        # check status code
        if forecast_hourly_response.status_code != 200:
            print('Error: ' + forecast_hourly_data['title'])
            return
        current_data = forecast_hourly_data['properties']['periods'][0]
        return nwsclass.Forecast(current_data)

    def get_hourly_forecast(self):
        "Get the forecast URL from the response"
        forecast_url = self.json['properties']['forecast']

        # Make another API request to the forecast URL with timeout set to 10 seconds
        forecast_response = requests.get(forecast_url, timeout=10)
        forecast_data = forecast_response.json()
        # check status code
        if forecast_response.status_code != 200:
            print('Error: ' + forecast_data['title'])
            return

        # create a list of forecasts
        forecasts = []
        # loop through forecast data and print out the forecast for each day
        for forecast in forecast_data['properties']['periods']:
            forecasts.append(nwsclass.Forecast(forecast))

        return forecasts


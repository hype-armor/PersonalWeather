# Gathers weather data from NWS API and returns it as a JSON object
import requests
import nwsclass
import UserPreferences

class NWS(object):
    "This class represents the NWS API"
    lat = ''
    lng = ''
    json = ''
    userperfs = UserPreferences.UserPreferences()
    currentWeather = nwsclass.HourlyForecast
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

        # Get the hourly forecast URL from the response
        forecast_hourly_url = self.json['properties']['forecastHourly']
        forecast_hourly_response = requests.get(forecast_hourly_url, timeout=10)
        forecast_hourly_data = forecast_hourly_response.json()
        # print the current weather
        current_data = forecast_hourly_data['properties']['periods'][0]
        start_time = current_data['startTime']
        end_time = current_data['endTime']
        temperature = current_data['temperature']
        windspeed = current_data['windSpeed']
        temperatureUnit = current_data['temperatureUnit']
        temperatureTrend = current_data['temperatureTrend']
        windSpeed = current_data['windSpeed']
        windDirection = current_data['windDirection']
        icon = current_data['icon']
        shortForecast = current_data['shortForecast']
        detailedForecast = current_data['detailedForecast']

        self.currentWeather = nwsclass.HourlyForecast(start_time, end_time, temperature, temperatureUnit, windspeed, windDirection, shortForecast, detailedForecast)


        

    def GetForecast(self):
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
            # print(forecast_date + ': ' + forecast['name'] + ': ' + forecast['detailedForecast'])

    def GetHourlyForecast(self):
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
            # print(forecast_date + ': ' + forecast['name'] + ': ' + forecast['detailedForecast'])


        # get the hourly forecast URL from the response
        hourly_forecast_url = self.json['properties']['forecastHourly']
        #print(hourly_forecast_url)

        # Make another API request to the hourly forecast URL with timeout set to 10 seconds
        hourly_forecast_response = requests.get(hourly_forecast_url, timeout=10)
        # check the status code
        if hourly_forecast_response.status_code != 200:
            print('Error: ' + str(hourly_forecast_response.status_code))
            return

        hourly_forecast_data = hourly_forecast_response.json()

        hourly_forecast = nwsclass.HourlyForecast(hourly_forecast_data['properties']['periods'][0]['startTime'], hourly_forecast_data['properties']['periods'][0]['endTime'], hourly_forecast_data['properties']['periods'][0]['temperature'], hourly_forecast_data['properties']['periods'][0]['temperatureUnit'], hourly_forecast_data['properties']['periods'][0]['windSpeed'], hourly_forecast_data['properties']['periods'][0]['windDirection'], hourly_forecast_data['properties']['periods'][0]['shortForecast'], hourly_forecast_data['properties']['periods'][0]['detailedForecast'])

        # set temperature and windspeed
        self.temperature = hourly_forecast.temperature
        # split the string at space and take the first element
        self.windspeed = int(hourly_forecast.wind_speed.split(' ')[0])

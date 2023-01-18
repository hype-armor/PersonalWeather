# Gathers weather data from NWS API and returns it as a JSON object

import requests
import nwsclass
import ziptolatlong

# get the latitude and longitude for the zip code
lat, lng = ziptolatlong.get('74037')

# Set up the API endpoint and parameters
endpoint = 'https://api.weather.gov/points/'

# Make the API request with timeout set to 10 seconds
response = requests.get(endpoint + lat + ',' + lng, timeout=10)

# Parse the JSON response
data = response.json()

# Get the forecast URL from the response
forecast_url = data['properties']['forecast']

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
hourly_forecast_url = data['properties']['forecastHourly']
#print(hourly_forecast_url)

# Make another API request to the hourly forecast URL with timeout set to 10 seconds
hourly_forecast_response = requests.get(hourly_forecast_url, timeout=10)
hourly_forecast_data = hourly_forecast_response.json()

hourly_forecast = nwsclass.HourlyForecast(hourly_forecast_data['properties']['periods'][0]['startTime'], hourly_forecast_data['properties']['periods'][0]['endTime'], hourly_forecast_data['properties']['periods'][0]['temperature'], hourly_forecast_data['properties']['periods'][0]['temperatureUnit'], hourly_forecast_data['properties']['periods'][0]['windSpeed'], hourly_forecast_data['properties']['periods'][0]['windDirection'], hourly_forecast_data['properties']['periods'][0]['shortForecast'], hourly_forecast_data['properties']['periods'][0]['detailedForecast'])

# print the hourly forecast for only the next 3 hours using a loop
for hourly_forecast in hourly_forecast_data['properties']['periods'][0:3]:
    # parse the forecast date and time
    forecast_date = hourly_forecast['startTime'].split('T')[1].split('-')[0]
    print(forecast_date + ': ' + hourly_forecast['shortForecast'] + ': ' + hourly_forecast['detailedForecast'])
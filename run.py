"run.py"
import nwsapi
import ziptolatlong
import UserPreferences

userperfs = UserPreferences.UserPreferences()

# Get the lat and long for the zip code
# miami fl 33195
# jenks ok 74037
zip = '74037'
location = ziptolatlong.get_location_information(zip)

print (location.place_name + ', ' + location.state_abbreviation)

# Create a new instance of the API
nws = nwsapi.NWS(location.latitude, location.longitude)
currentWeather = nws.get_current_weather()

CURRENT_WEATHER = ""
if currentWeather.temperature >= 78:
    # take whichever is higher, the heat index or the wbgt
    import wbgt
    nwswbgt = wbgt.WBGT(location.latitude, location.longitude)
    feelslike, heatindex = nwswbgt.update()
    if feelslike > heatindex:
        CURRENT_WEATHER = 'WBGT ' + userperfs.checkTemp(feelslike)
    else:
        CURRENT_WEATHER = 'Heat Index  ' + userperfs.checkTemp(heatindex)

elif currentWeather.temperature >= 45 and currentWeather.temperature <= 77 or \
        (currentWeather.temperature >= 45 and currentWeather.wind_speed < 3):
    CURRENT_WEATHER = 'Temperature ' + userperfs.checkTemp(currentWeather.temperature)

elif currentWeather.temperature > -45 and currentWeather.temperature < 45 and \
    currentWeather.wind_speed >= 3:
    import windchill
    f,c,w = windchill.CalculateWindChill(currentWeather.temperature, \
        currentWeather.wind_speed)
    CURRENT_WEATHER = 'Windchill ' + userperfs.checkTemp(f)

print (CURRENT_WEATHER)

forecasts = nws.get_hourly_forecast()
FORECASTED_WEATHER = ""
for forecast in forecasts:
    #print (forecast.name + ': ' + forecast.detailed_forecast)
    if forecast.is_daytime:
        FORECASTED_WEATHER = "<p>" + forecast.name + ": " + forecast.short_forecast + ', with a high around ' + \
            str(userperfs.checkTemp(forecast.temperature)) + "</p>"
    else:
        FORECASTED_WEATHER = "<p>" + forecast.name + ": " + forecast.short_forecast + ', with a low around ' + \
            str(userperfs.checkTemp(forecast.temperature)) + "</p>"
    

import json

def open_file(filename, type):
    with open(filename, 'r') as f:
        return f.read()

data = {}
data['product'] = "Greg's Magical Weather api"
data['version'] = 0.1
data['releaseDate'] = "2023-01-22T00:00:00.000Z"
data['author'] = "Gregory A. Morgan Garcia"

location_json = {}
for item in vars(location):
    location_json[item] = getattr(location, item)
data['location'] = location_json

weather = {}
current_conditions = {}
for item in vars(currentWeather):
    current_conditions[item] = getattr(currentWeather, item)

current_conditions['feels_like'] = CURRENT_WEATHER
weather['current_conditions'] = current_conditions
data['weather'] = weather

forecast_json = {}
conditions = []
for forecast in forecasts:
    condition = {}
    for item in vars(forecast):
        condition[item] = getattr(forecast, item)
    conditions.append(condition)
conditions.append(condition)
forecast_json['conditions'] = conditions
data['forecast'] = forecast_json

json_data = json.dumps(data)


from flask import Flask
from flask import Response
from flask import render_template, send_from_directory

app = Flask(__name__)

@app.route("/")
def hello_world():
    return Response(open_file("web/html/index.html", "html"), mimetype='text/html')

@app.route("/js/<path:path>")
def send_js(path):
    return Response(open_file("web/js/"+path, "js"), mimetype='application/javascript')

@app.route("/api")
def api():
    return Response(json_data, mimetype='application/json')
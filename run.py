"run.py"
import nwsapi
import ziptolatlong
import UserPreferences

userperfs = UserPreferences.UserPreferences()

# Get the lat and long for the zip code
# miami fl 33195
# jenks ok 74037
location = ziptolatlong.get_location_information('74037')

print (location.place_name + ', ' + location.state_abbreviation)

# Create a new instance of the API
nws = nwsapi.NWS(location.latitude, location.longitude)
currentWeather = nws.get_current_weather()
print()
print ("Now: ", end="")
if currentWeather.temperature >= 78:
    # take whichever is higher, the heat index or the wbgt
    import wbgt
    nwswbgt = wbgt.WBGT(location.latitude, location.longitude)
    feelslike, heatindex = nwswbgt.update()
    print (feelslike)
    print (heatindex)
    if feelslike > heatindex:
        print ('WBGT ' + userperfs.checkTemp(feelslike))
    else:
        print ('Heat Index  ' + userperfs.checkTemp(heatindex))

elif currentWeather.temperature >= 45 and currentWeather.temperature <= 77 or \
        (currentWeather.temperature >= 45 and currentWeather.wind_speed < 3):
    print (str(currentWeather.temperature) + '°' + currentWeather.temperature_unit + ' ' + currentWeather.short_forecast)
    print ('Temperature ' + userperfs.checkTemp(currentWeather.temperature))

elif currentWeather.temperature > -45 and currentWeather.temperature < 45 and \
    currentWeather.wind_speed >= 3:
    import windchill
    f,c,w = windchill.CalculateWindChill(currentWeather.temperature, \
        currentWeather.wind_speed)
    print ('Windchill ' + userperfs.checkTemp(f))

print()
forecasts = nws.get_hourly_forecast()
for forecast in forecasts:
    #print (forecast.name + ': ' + forecast.detailed_forecast)
    if forecast.is_daytime:
        print (forecast.name + ": " + forecast.short_forecast + ', with a high around ' + \
            str(userperfs.checkTemp(forecast.temperature)))
    else:
        print (forecast.name + ": " + forecast.short_forecast + ', with a low around ' + \
            str(userperfs.checkTemp(forecast.temperature)))
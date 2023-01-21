"run.py"
import nwsapi
import ziptolatlong
import UserPreferences

userperfs = UserPreferences.UserPreferences()

# Get the lat and long for the zip code
lat, lng = ziptolatlong.get('30030')

# Create a new instance of the API
nws = nwsapi.NWS(lat, lng)
currentWeather = nws.get_current_weather()
forecasts = nws.get_hourly_forecast()

if currentWeather.temperature >= 78:
    # take whichever is higher, the heat index or the wbgt
    import wbgt
    nwswbgt = wbgt.WBGT(nws.lat, nws.lng)
    feelslike, heatindex = nwswbgt.update()
    print (feelslike)
    print (heatindex)
    if feelslike > heatindex:
        print ('WBGT ' + userperfs.checkTemp(feelslike))
    else:
        print ('Heat Index  ' + userperfs.checkTemp(heatindex))
elif currentWeather.temperature >= 45 and currentWeather.temperature <= 77 or \
        (currentWeather.temperature >= 45 and currentWeather.wind_speed < 3):
    print (currentWeather.temperature)
    print ('Temperature ' + userperfs.checkTemp(currentWeather.temperature))
elif currentWeather.temperature > -45 and currentWeather.temperature < 45 and \
    currentWeather.wind_speed >= 3:
    import windchill
    f,c,w = windchill.CalculateWindChill(currentWeather.temperature, currentWeather.wind_speed)
    print (f)
    print ('Windchill ' + userperfs.checkTemp(f))

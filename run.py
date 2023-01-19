"run.py"
import nwsapi
import ziptolatlong

# Get the lat and long for the zip code
lat, lng = ziptolatlong.get('74037')

# Create a new instance of the API
nws = nwsapi.NWS(lat, lng)
#nws.GetForecast()
#nws.GetHourlyForecast()

if nws.currentWeather.temperature >= 78:
    # take whichever is higher, the heat index or the wbgt
    import wbgt
    nwswbgt = wbgt.WBGT(nws.lat, nws.lng)
    feelslike, heatindex = nwswbgt.update()
    print (feelslike)
    print (heatindex)
    if feelslike > heatindex:
        print ('WBGT ' + nws.userperfs.checkTemp(feelslike))
    else:
        print ('Heat Index  ' + nws.userperfs.checkTemp(heatindex))
elif nws.currentWeather.temperature >= 45 and nws.currentWeather.temperature <= 77 or \
        (nws.currentWeather.temperature >= 45 and nws.windspeed < 3):
    print (nws.currentWeather.temperature)
    print ('Temperature ' + nws.userperfs.checkTemp(nws.currentWeather.temperature))
elif nws.currentWeather.temperature > -45 and nws.currentWeather.temperature < 45 and nws.windspeed >= 3:
    import windchill
    f,c,w = windchill.CalculateWindChill(nws.currentWeather.temperature, nws.windspeed)
    print (f)
    print ('Windchill ' + nws.userperfs.checkTemp(f))

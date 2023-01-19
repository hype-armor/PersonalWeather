import nwsapi

# Create a new instance of the API
nws = nwsapi.nws('90210')
nws.GetForecast()
nws.GetHourlyForecast()

if nws.temperature >= 78:
    import wbgt
    object = wbgt.wbgt(nws.lat, nws.lng)
    if object.feelslike > object.heatindex:
        print (object.feelslike)
        print ('WBGT ' + nws.userperfs.checkTemp(object.feelslike))
    else:
        print (object.heatindex)
        print ('Heat Index  ' + nws.userperfs.checkTemp(object.heatindex))
elif nws.temperature >= 46 and nws.temperature <= 77 or (nws.temperature >= 46 and nws.windspeed < 3):
    print (nws.temperature)
    print ('Temperature ' + nws.userperfs.checkTemp(nws.temperature))
elif nws.temperature > -45 and nws.temperature < 45 and nws.windspeed >= 3:
    import windchill
    f,c,w = windchill.CalculateWindChill(nws.temperature, nws.windspeed)
    print (f)
    print ('Windchill ' + nws.userperfs.checkTemp(f))
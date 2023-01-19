import nwsapi

# Create a new instance of the API
nws = nwsapi.nws('74037')
nws.GetForecast()
nws.GetHourlyForecast()



import wbgt
object = wbgt.wbgt(nws.lat, nws.lng)
print (object.feelslike)
print (object.heatindex)
print ('With WBGT' + ' ' + nws.userperfs.checkTemp(object.feelslike))
print ('With HI  ' + ' ' + nws.userperfs.checkTemp(object.heatindex))

# get windchill
import windchill
f,c,w = windchill.CalculateWindChill(nws.temperature, nws.windspeed)
print (f)
print ('With WC  ' + ' ' + nws.userperfs.checkTemp(f))
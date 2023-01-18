import nwsapi

# Create a new instance of the API
nws = nwsapi.nws('74037')
nws.GetForecast()
nws.GetHourlyForecast()
import nwsapi

# Create a new instance of the API
nws = nwsapi.nws('74037')
nws.GetForecast()
nws.GetHourlyForecast()

import wbgt
object = wbgt.wbgt(36.0148, -95.9797, 700)


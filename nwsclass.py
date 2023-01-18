# create a python class to hold the hourly forecast data
class HourlyForecast:
    def __init__(self, start_time, end_time, temperature, temperature_unit, wind_speed, wind_direction, short_forecast, detailed_forecast):
        self.start_time = start_time
        self.end_time = end_time
        self.temperature = temperature
        self.temperature_unit = temperature_unit
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        #self.wind_direction_compass = wind_direction_compass
        self.short_forecast = short_forecast
        self.detailed_forecast = detailed_forecast
"This module contains the HourlyForecast class and the get_special_forecast method."

class Forecast:
    "This class represents a single hourly forecast from the NWS API"
    def __init__(self, current_data):
        "Initialize the HourlyForecast class"
        self.number = current_data['number']
        self.name = current_data['name']
        self.start_time = current_data['startTime']
        self.end_time = current_data['endTime']
        self.is_daytime = current_data['isDaytime']
        self.temperature = current_data['temperature']
        self.temperature_unit = current_data['temperatureUnit']
        self.temperature_trend = current_data['temperatureTrend']
        if len(current_data['windSpeed'].split(' ')) > 2:
            self.wind_speed = int(current_data['windSpeed'].split(' ')[2])
        else:
            self.wind_speed = int(current_data['windSpeed'].split(' ')[0])
        self.wind_speed_text = current_data['windSpeed']
        self.wind_direction = current_data['windDirection']
        self.icon = current_data['icon']
        self.short_forecast = current_data['shortForecast']
        self.detailed_forecast = current_data['detailedForecast']
        self.feels_like = ""

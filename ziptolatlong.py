"""Get the latitude and longitude for a zip code"""
import requests

class location(object):
    "This class represents the location object"
    def __init__(self, data):
        place = data['places'][0]
        self.latitude = place['latitude']
        self.longitude = place['longitude']
        self.state = place['state']
        self.state_abbreviation = place['state abbreviation']
        self.place_name = place['place name']

def get_location_information(zip_code):
    "Get the latitude and longitude for a zip code"
    # Set up the API endpoint and parameters
    endpoint = 'https://api.zippopotam.us/us/'

    # Make the API request
    response = requests.get(endpoint + zip_code, timeout=10)

    return location(response.json())

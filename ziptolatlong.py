import requests

def get(zip_code):
    # Set up the API endpoint and parameters
    endpoint = 'https://api.zippopotam.us/us/'
    zip_code = zip_code

    # Make the API request
    response = requests.get(endpoint + zip_code, timeout=10)

    # Parse the JSON response
    data = response.json()

    # Get the latitude and longitude from the response
    lat = data.get('places')[0].get('latitude')
    lng = data.get('places')[0].get('longitude')

    # Print the latitude and longitude
    print(f'Latitude: {lat}, Longitude: {lng}')

    return lat, lng

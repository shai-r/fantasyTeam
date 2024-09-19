import requests

def get_data(url):
    response = requests.request('Get', url)
    return response.json()
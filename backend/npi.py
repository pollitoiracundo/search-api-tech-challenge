import json
import urllib.parse
import requests

def get_npi_query(json_data):
    # Parse the JSON string if it's a string, otherwise assume it's a dictionary
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data

    # Construct the URL parameters
    url_params = urllib.parse.urlencode(data)

    # Construct the URL
    base_url = "https://npiregistry.cms.hhs.gov/api/?"
    full_url = base_url + url_params
    
    return full_url

def make_npi_api_call(url):
    response = requests.get(url)   
    return response.json()


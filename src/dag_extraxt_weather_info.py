from pprint import pprint

import requests

# beschikbaar tot 1 juli 2023
API_KEY = 'eyJvcmciOiI1ZTU1NGUxOTI3NGE5NjAwMDEyYTNlYjEiLCJpZCI6IjI4ZWZlOTZkNDk2ZjQ3ZmE5YjMzNWY5NDU3NWQyMzViIiwiaCI6Im11cm11cjEyOCJ9'

url = "https://api.dataplatform.knmi.nl/open-data/v1/datasets/Actuele10mindataKNMIstations/versions/2/files"

result = requests.get(url=url, params={'maxResults': 100}, headers={'Authorization': API_KEY})
print(result.request.url)

if result.status_code == 200:
    available_dataset = result.json()
    pprint(available_dataset)
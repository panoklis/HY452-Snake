import requests

# Make a GET request to a JSON API
response = requests.get('https://wl2uxwpe15.execute-api.us-east-1.amazonaws.com/test/theme')
# Parse and print the JSON response
if response.status_code == 200:  # Check if the request was successful
    print(response.json())
    print(f'Content type: {response.headers["content-type"]}')

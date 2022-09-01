'''
spotify settings
'''

import base64
import json
import requests

client_id = "44094eff54094a27b593823d350416e6"
client_secret = "2a6665093d3d4f54bf887b719766f919"
endpoint = "https://accounts.spotify.com/api/token"

encoded = base64.b64encode("{}:{}".format(
    client_id, client_secret).encode('utf-8')).decode('ascii')
headers = {"Authorization": "Basic {}".format(encoded)}
payload = {"grant_type": "client_credentials"}
response = requests.post(endpoint, data=payload, headers=headers)
access_token = json.loads(response.text)['access_token']
headers = {"Authorization": "Bearer {}".format(access_token)}

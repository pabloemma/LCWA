import base64
import requests
import json

APP_KEY = '70yem8c9kt0r29f'
APP_SECRET = 'sbm9401ugpfasgp'
ACCESS_CODE_GENERATED = '1N74OZNee0AAAAAAAAAG_JxGE4PDJF_RgMrMwRKWyY0'

BASIC_AUTH = base64.b64encode(f'{APP_KEY}:{APP_SECRET}'.encode())

headers = {
    'Authorization': f"Basic {BASIC_AUTH}",
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = f'code={ACCESS_CODE_GENERATED}&grant_type=authorization_code'

response = requests.post('https://api.dropboxapi.com/oauth2/token',
                         data=data,
                         auth=(APP_KEY, APP_SECRET))
print(json.dumps(json.loads(response.text), indent=2))
import jwt
import os
import requests
import uuid
from urllib.parse import urlencode, unquote


access_key, secret_key = [k.split(':')[-1] for k in open('../secret_api_keys.txt').read().split('\n')]
server_url = 'https://api.upbit.com'

def get_my_accounts():
  payload = {
      'access_key': access_key,
      'nonce': str(uuid.uuid4()),
  }
  jwt_token = jwt.encode(payload, secret_key)
  authorization = 'Bearer {}'.format(jwt_token)
  headers = {
    'Authorization': authorization,
  }

  res = requests.get(server_url + '/v1/accounts', params=None, headers=headers)
  return res.json()

if __name__ == "__main__":
  print(get_my_accounts())
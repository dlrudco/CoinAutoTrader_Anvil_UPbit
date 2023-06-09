import jwt
import requests
import uuid as uuidlib
from dataclasses import dataclass

__all__ = ['get_my_balance', 'credentials']

access_key, secret_key = [k.split(':')[-1] for k in open('secret_api_keys.txt').read().split('\n')]
server_url = 'https://api.upbit.com'

@dataclass(frozen=True)
class credentials:
  access_key = access_key
  secret_key = secret_key
  server_url = server_url
  def __repr__(self):
    return f'access_key: {self.access_key}, secret_key: {self.secret_key}'

  def __dict__(self):
    return {'access_key': self.access_key, 'secret_key': self.secret_key}
  
def get_my_balance():
  payload = {
      'access_key': access_key,
      'nonce': str(uuidlib.uuid4()),
  }
  jwt_token = jwt.encode(payload, secret_key)
  authorization = 'Bearer {}'.format(jwt_token)
  headers = {
    'Authorization': authorization,
  }

  res = requests.get(server_url + '/v1/accounts', params=None, headers=headers)
  return {**res.json(), 'headers':{**res.headers}}

if __name__ == "__main__":
  print(credentials().access_key)
  print(get_my_balance())
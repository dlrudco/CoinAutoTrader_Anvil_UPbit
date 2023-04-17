import jwt
from urllib.parse import urlencode, unquote
import hashlib
import uuid as uuidlib

from InformationHandler import credentials
creds = credentials()

def encode_payload(params):
    query_string = unquote(urlencode(params, doseq=True)).encode("utf-8")

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': creds.access_key,
        'nonce': str(uuidlib.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, creds.secret_key)
    authorization = 'Bearer {}'.format(jwt_token)
    headers = {
    'Authorization': authorization,
    }
    return headers
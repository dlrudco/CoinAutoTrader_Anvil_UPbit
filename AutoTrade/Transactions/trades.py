import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from InformationHandler import *

import jwt
import hashlib
import requests
import uuid as uuidlib
from urllib.parse import urlencode, unquote

creds = credentials()

__all__ = ['limit_sell_coin', 'limit_buy_coin', 'market_sell_coin', 'market_buy_coin', 'cancel_order']

def post_order(market:str, side:str, ord_type:str, price:float, volume:float):
    """_summary_

    :param market: _description_
    :type market: str
    :param side: _description_
    :type side: str
    :param ord_type: _description_
    :type ord_type: str
    :param price: _description_
    :type price: float
    :param volume: _description_
    :type volume: float
    :return: 
        uuid	주문의 고유 아이디	String
        side	주문 종류	String
        ord_type	주문 방식	String
        price	주문 당시 화폐 가격	NumberString
        state	주문 상태	String
        market	마켓의 유일키	String
        created_at	주문 생성 시간	String
        volume	사용자가 입력한 주문 양	NumberString
        remaining_volume	체결 후 남은 주문 양	NumberString
        reserved_fee	수수료로 예약된 비용	NumberString
        remaining_fee	남은 수수료	NumberString
        paid_fee	사용된 수수료	NumberString
        locked	거래에 사용중인 비용	NumberString
        executed_volume	체결된 양	NumberString
        trades_count	해당 주문에 걸린 체결 수	Integer
    :rtype: _type_
    """
    params = {
    'market': market,
    'side': side,
    'ord_type': ord_type,
    'price': price,
    'volume': volume
    }
    if params['price'] is None:
        del params['price']
        
    
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

    res = requests.post(creds.server_url + '/v1/orders', json=params, headers=headers)
    return res.json()

def limit_sell_coin(market, price, volume):
    return post_order(market, 'ask', 'limit', price, volume)

def limit_buy_coin(market, price, volume):
    return post_order(market, 'bid', 'limit', price, volume)

def market_sell_coin(market, volume):
    return post_order(market, 'ask', 'market', None, volume)

def market_buy_coin(market, volume):
    return post_order(market, 'bid', 'price', None, volume)

def cancel_order(uuid:str=None, identifier:str=None):
    assert uuid or identifier, 'uuid or identifier must be provided'
    assert not (uuid and identifier), 'uuid and identifier cannot be provided at the same time'


    params = {'uuid': uuid} if uuid else {'identifier': identifier}
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

    res = requests.delete(creds.server_url + '/v1/order', params=params, headers=headers)
    return res.json()

if __name__ == "__main__":
    breakpoint()
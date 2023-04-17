import os
if __name__ == "__main__":
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from InformationHandler import *
from utils import payload, header

import time
import requests

creds = credentials()

__all__ = ['limit_sell_coin', 'limit_buy_coin', 'market_sell_coin', 'market_buy_coin', 'cancel_order']

def post_order(market:str, side:str, ord_type:str, price:float, volume:float):
    """주어진 파라미터에 상응하는 거래를 요청한다

    :param market: 거래를 요청할 마켓코드
    :type market: str
    :param side: 매수('bid')/매도('ask') 구분
    :type side: str
    :param ord_type: 시장가 주문('market/price')/지정가 주문('limit') 구분
    :type ord_type: str
    :param price: 거래 가격
    :type price: float
    :param volume: 거래 물량
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
    if params['volume'] is None:
        del params['volume']
    
    headers = payload.encode_payload(params)

    res = requests.post(creds.server_url + '/v1/orders', json=params, headers=headers)
    return {**res.json(), 'headers':{**res.headers}}

def limit_sell_coin(market, price, volume):
    return post_order(market, 'ask', 'limit', price, volume)

def limit_buy_coin(market, price, volume):
    return post_order(market, 'bid', 'limit', price, volume)

def market_sell_coin(market, volume):
    return post_order(market, 'ask', 'market', None, volume)

def market_buy_coin(market, price):
    return post_order(market, 'bid', 'price', price, None)

def cancel_order(uuid:str=None, identifier:str=None):
    assert uuid or identifier, 'uuid or identifier must be provided'
    assert not (uuid and identifier), 'uuid and identifier cannot be provided at the same time'


    params = {'uuid': uuid} if uuid else {'identifier': identifier}
    headers = payload.encode_payload(params)

    res = requests.delete(creds.server_url + '/v1/order', params=params, headers=headers)
    return {**res.json(), 'headers':{**res.headers}}

def cancel_all_waiting(market):
    order_list = check_all_orders_by_state(market, 'wait')
    flag = True
    for o in order_list:
        if flag:
            stat = cancel_order(uuid=o['uuid'])
            print(o['uuid'], stat['state'])
        if header.get_remaining_calls(stat['headers'])['lim_second'] ==0 or header.get_remaining_calls(stat['headers'])['lim_minute'] ==0:
            time.sleep(0.1)
            flag = False
        else:
            flag = True
            

if __name__ == "__main__":
    breakpoint()